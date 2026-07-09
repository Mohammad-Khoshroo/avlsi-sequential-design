import os
import re
import math
import json
import logging

# ==========================================================
# CONFIG
# ==========================================================

BASE_DIR = "./simulation/combinational-circuit"
FILE_PATTERN = r"\.mt[a-zA-Z0-9]+$"
OUTPUT_JSON_NAME = "measure.json"

SUMMARIZE = True

SIGNALS = ["A", "B", "Cin"]

# Headers that are control/metadata, not measurements or delays
CONTROL_HEADERS = {"index", "alter#", "temp", "temper", "is_fall_transition"}

# ==========================================================

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def scientific_to_si(val):
    if not isinstance(val, (int, float)):
        return str(val)
    if val == 0:
        return "0"

    si_prefixes = {
        24: "Y", 21: "Z", 18: "E", 15: "P", 12: "T",
        9: "G", 6: "M", 3: "k", 0: "",
        -3: "m", -6: "µ", -9: "n", -12: "p", -15: "f",
        -18: "a", -21: "z", -24: "y",
    }

    exponent = math.floor(math.log10(abs(val)))
    si_exp = (exponent // 3) * 3
    si_exp = max(min(si_exp, 24), -24)
    scaled = val / (10 ** si_exp)
    return f"{scaled:g}{si_prefixes[si_exp]}"


def clean_value(val_str):
    val_str = val_str.strip().lower()
    if val_str in ("failed", "fail", ""):
        return None
    try:
        return float(val_str)
    except ValueError:
        return val_str


def parse_single_mt_file(filepath):
    """Tokenize an HSPICE .mt* file into (headers, records).

    Works for both:
      - delay-style files (with a_init/a_final, tplh_*, tphl_*)
      - sweep-style files (t_setup vs q_max, etc.)
    """
    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        lines = f.readlines()

    tokens = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        upper = line.upper()
        if upper.startswith(".TITLE"):
            continue
        if upper.startswith("$DATA"):
            continue
        tokens.extend(line.split())

    if not tokens:
        return None

    # Collect header tokens until we hit the first numeric token.
    headers = []
    i = 0
    while i < len(tokens):
        token = tokens[i]
        try:
            float(token)
            break
        except ValueError:
            pass
        if token.lower() in ("failed", "fail"):
            break
        headers.append(token.lower())
        i += 1

    if not headers:
        return None

    data_tokens = tokens[i:]
    record_len = len(headers)
    records = []

    for start in range(0, len(data_tokens) - record_len + 1, record_len):
        chunk = data_tokens[start: start + record_len]
        rec = {h: clean_value(v) for h, v in zip(headers, chunk)}
        records.append(rec)

    return records


# ==========================================================
# File-type detection
# ==========================================================

def is_sweep_file(records):
    """A sweep file has no <sig>_init / <sig>_final columns for any signal."""
    if not records:
        return False
    sample = records[0]
    for sig in SIGNALS:
        s = sig.lower()
        if f"{s}_init" in sample and f"{s}_final" in sample:
            return False
    return True


def detect_sweep_parameter(records):
    """Heuristic: first non-control column that varies across rows is the swept param."""
    if not records:
        return None
    sample = records[0]
    candidates = [
        k for k in sample.keys()
        if k not in CONTROL_HEADERS
        and not k.endswith("_init")
        and not k.endswith("_final")
        and not k.startswith("tplh_")
        and not k.startswith("tphl_")
    ]
    for k in candidates:
        vals = [r.get(k) for r in records]
        if any(v != vals[0] for v in vals):
            return k
    return candidates[0] if candidates else None


# ==========================================================
# Delay-style processing (original logic, lightly refactored)
# ==========================================================

def build_test_name(rec):
    transition_signal = None
    transition_from = None
    transition_to = None
    static_inputs = []

    for sig in SIGNALS:
        s = sig.lower()
        init_key = f"{s}_init"
        final_key = f"{s}_final"
        if init_key not in rec:
            continue

        init_val = rec.get(init_key)
        final_val = rec.get(final_key)

        if init_val != final_val:
            transition_signal = sig
            transition_from = int(init_val)
            transition_to = int(final_val)
        else:
            static_inputs.append(f"{sig}={int(init_val)}")

    if transition_signal is None:
        return "UNKNOWN"

    return (
        f"{transition_signal}:"
        f"{transition_from}->{transition_to}"
        f" | "
        f"{' '.join(static_inputs)}"
    )


def build_delay_summary(output_data):
    summary = {"delay": {}, "measurements": {}}

    delay_values = {}
    measurement_values = {}

    for test in output_data.values():
        if not isinstance(test, dict):
            continue
        for name, val in test.get("delay", {}).items():
            if val is None:
                continue
            delay_values.setdefault(name, []).append(val)
        for name, val in test.get("measurements", {}).items():
            if isinstance(val, (int, float)):
                measurement_values.setdefault(name, []).append(val)

    # ---- per-delay-name stats + aggregated tplh_/tphl_/t_p_ per output ----
    output_dirs = {}

    for name, values in delay_values.items():
        summary["delay"][name] = {
            "min": min(values),
            "max": max(values),
            "avg": sum(values) / len(values),
        }
        parts = name.split("_")
        if len(parts) >= 3:
            dir_type = parts[0]      # tplh or tphl
            out_sig = parts[1]       # output signal
            if out_sig not in output_dirs:
                output_dirs[out_sig] = {"tplh": [], "tphl": []}
            if dir_type in ("tplh", "tphl"):
                output_dirs[out_sig][dir_type].extend(values)

    for out_sig, dirs in output_dirs.items():
        if dirs["tplh"]:
            summary["delay"][f"tplh_{out_sig}"] = {
                "min": min(dirs["tplh"]),
                "max": max(dirs["tplh"]),
                "avg": sum(dirs["tplh"]) / len(dirs["tplh"]),
            }
        if dirs["tphl"]:
            summary["delay"][f"tphl_{out_sig}"] = {
                "min": min(dirs["tphl"]),
                "max": max(dirs["tphl"]),
                "avg": sum(dirs["tphl"]) / len(dirs["tphl"]),
            }
        all_out = dirs["tplh"] + dirs["tphl"]
        if all_out:
            summary["delay"][f"t_p_{out_sig}"] = {
                "min": min(all_out),
                "max": max(all_out),
                "avg": sum(all_out) / len(all_out),
            }

    for name, values in measurement_values.items():
        summary["measurements"][name] = {
            "min": min(values),
            "max": max(values),
            "avg": sum(values) / len(values),
        }

    all_delays = []
    for vals in delay_values.values():
        all_delays.extend(vals)
    if all_delays:
        summary["worst_case_delay"] = max(all_delays)
        summary["best_case_delay"] = min(all_delays)
        summary["avg_case_delay"] = sum(all_delays) / len(all_delays)

    return summary


def process_delay_records(records):
    if not records:
        return {}

    all_keys = set()
    for rec in records:
        all_keys.update(rec.keys())

    meas_headers = sorted(list(all_keys - CONTROL_HEADERS))
    output_data = {}

    for rec in records:
        idx = rec.get("index")
        if idx is None:
            idx = rec.get("alter#", "unknown")
        idx_str = str(int(idx)) if isinstance(idx, float) else str(idx)

        transition = {}
        state = {}
        transition_signal = None

        for sig in SIGNALS:
            s = sig.lower()
            init_key = f"{s}_init"
            final_key = f"{s}_final"
            if init_key not in rec or final_key not in rec:
                continue
            init_val = rec[init_key]
            final_val = rec[final_key]
            if init_val != final_val:
                transition_signal = s
                transition = {
                    "signal": sig,
                    "from": int(init_val),
                    "to": int(final_val),
                }
            else:
                state[sig] = int(init_val)

        delay = {}
        measurements = {}

        for key in meas_headers:
            lower_key = key.lower()
            if lower_key.endswith("_init") or lower_key.endswith("_final"):
                continue

            is_delay = lower_key.startswith("tplh_") or lower_key.startswith("tphl_")
            val = rec.get(key)

            if is_delay:
                if transition_signal is None:
                    continue
                if not lower_key.endswith("_" + transition_signal):
                    continue
                delay[key] = val
            else:
                if not isinstance(val, float):
                    continue
                measurements[key] = val

        output_data[idx_str] = {
            "transition": transition,
            "state": state,
            "delay": delay,
            "measurements": measurements,
        }

    if SUMMARIZE:
        output_data["summary"] = build_delay_summary(output_data)

    return output_data


# ==========================================================
# Sweep-style processing (NEW)
# ==========================================================

def build_sweep_summary(rows, sweep_param):
    """For a sweep file: stats on each numeric column + sweep extremes."""
    summary = {"sweep_parameter": sweep_param, "measurements": {}}

    numeric_cols = {}
    for row in rows:
        for name, val in row.get("measurements", {}).items():
            if isinstance(val, (int, float)):
                numeric_cols.setdefault(name, []).append(val)

    for name, values in numeric_cols.items():
        summary["measurements"][name] = {
            "min": min(values),
            "max": max(values),
            "avg": sum(values) / len(values),
        }

    # Identify sweep extremes (useful for finding critical setup time, etc.)
    if sweep_param and sweep_param in numeric_cols:
        sp_vals = numeric_cols[sweep_param]
        summary["sweep_range"] = {
            "start": sp_vals[0],
            "end": sp_vals[-1],
            "min": min(sp_vals),
            "max": max(sp_vals),
            "step": (sp_vals[1] - sp_vals[0]) if len(sp_vals) > 1 else None,
        }

    return summary


def process_sweep_records(records):
    """Process a sweep-style .mt file (e.g. t_setup vs q_max).

    Each row becomes one entry, keyed by a unique per-row id (alter# + row#),
    so rows with the same alter# no longer overwrite each other.
    """
    if not records:
        return {}

    sweep_param = detect_sweep_parameter(records)
    output_data = {}

    last_alter = None
    row_in_alter = 0
    for i, rec in enumerate(records):
        alter = rec.get("alter#")
        if alter is not None:
            if alter != last_alter:
                last_alter = alter
                row_in_alter = 0
            else:
                row_in_alter += 1
            alter_int = int(alter) if isinstance(alter, float) else alter
            idx_str = f"{alter_int}_{row_in_alter}"
        else:
            idx_str = str(i)

        measurements = {}
        for key, val in rec.items():
            if key.lower() in CONTROL_HEADERS:
                continue
            if val is None:
                continue
            measurements[key] = val

        entry = {
            "type": "sweep",
            "sweep_parameter": sweep_param,
            "measurements": measurements,
        }
        output_data[idx_str] = entry

    if SUMMARIZE:
        output_data["summary"] = build_sweep_summary(
            list(output_data.values()), sweep_param
        )

    return output_data


# ==========================================================
# Dispatcher
# ==========================================================

def process_records(records):
    if not records:
        return {}
    if is_sweep_file(records):
        return process_sweep_records(records)
    return process_delay_records(records)


# ==========================================================
# Main
# ==========================================================

def main():
    print("=== Processing HSPICE Results ===")
    target_dir = os.path.abspath(BASE_DIR)

    if not os.path.isdir(target_dir):
        print(f"Directory not found:\n{target_dir}")
        return

    processed_count = 0
    for root, _, files in os.walk(target_dir):
        for file in files:
            if not re.search(FILE_PATTERN, file.lower()):
                continue

            filepath = os.path.join(root, file)
            print(f"Parsing: {filepath}")

            recs = parse_single_mt_file(filepath)
            if not recs:
                continue

            file_kind = "sweep" if is_sweep_file(recs) else "delay"
            print(f"   detected: {file_kind} file, {len(recs)} rows")

            result = process_records(recs)

            base_name, ext = os.path.splitext(file)
            output_name = (
                f"{base_name}_{ext.replace('.', '')}_{OUTPUT_JSON_NAME}"
            )
            output_path = os.path.join(root, output_name)

            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(result, f, indent=4, ensure_ascii=False)

            print(f"-> Saved JSON to: {output_path}")
            processed_count += 1

    if processed_count == 0:
        print("No MT results found to process.")
    else:
        print(f"\nSuccessfully processed {processed_count} files.")


if __name__ == "__main__":
    main()
