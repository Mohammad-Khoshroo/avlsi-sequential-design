import os
import json
import numpy as np
import matplotlib.pyplot as plt

# ==========================================================
# CONFIG
# ==========================================================

TARGET_DIRS = [
    r"simulation/pipe/2latch/sim_mt0_measure.json",
]

LEGEND_LABELS = [
    "25°C",
]

# --- What to plot -------------------------------------------------
# "t بر حسب Q"  ->  t on Y-axis, Q on X-axis.
# Swap these two if you want the conventional Q(t) orientation instead.
X_PARAM  = "tc"     # X-axis measurement key
Y_PARAM  = "out_min"   # Y-axis measurement key
X_UNIT   = "s"         # unit symbol for X (empty string to omit)
Y_UNIT   = "V"         # unit symbol for Y (will be SI-prefixed: p, n, µ, m ...)

OUTPUT_FILE = "t_vs_q_plot.png"

COLORS = [
    "#636EFA", "#EF553B", "#00CC96", "#AB63FA", "#FFA15A",
    "#19D3F3", "#FF6692", "#B6E880", "#FF97FF", "#FECB52",
    "#1F77B4", "#FF7F0E", "#2CA02C", "#D62728", "#9467BD", "#8C564B",
]

# ==========================================================
# Helpers
# ==========================================================

def auto_scale(values):
    """Pick an SI prefix so axis numbers are human-readable."""
    if not values:
        return 1.0, ""
    abs_vals = [abs(v) for v in values if v != 0]
    if not abs_vals:
        return 1.0, ""
    mean_exp = np.mean([int(np.floor(np.log10(v))) for v in abs_vals])
    if mean_exp < -10:
        return 1e12, "p"
    if mean_exp < -7:
        return 1e9,  "n"
    if mean_exp < -4:
        return 1e6,  "µ"
    if mean_exp < -1:
        return 1e3,  "m"
    return 1.0, ""


def format_label(param, prefix, unit):
    if prefix and unit:
        return f"{param} ({prefix}{unit})"
    if unit:
        return f"{param} ({unit})"
    if prefix:
        return f"{param} ({prefix})"
    return param


def extract_sweep_pairs(file_data, x_key, y_key):
    """Walk every 'type': 'sweep' entry in measure.json and collect (x, y) pairs.
    Skips 'summary' and any non-sweep entries."""
    pairs = []
    for entry_key, entry in file_data.items():
        if entry_key == "summary":
            continue
        if not isinstance(entry, dict):
            continue
        if entry.get("type") != "sweep":
            continue
        meas = entry.get("measurements", {})
        if x_key not in meas or y_key not in meas:
            continue
        x, y = meas[x_key], meas[y_key]
        if x is None or y is None:
            continue
        pairs.append((float(x), float(y)))
    # Sort by X so the connecting line follows sweep order, not file order
    pairs.sort(key=lambda p: p[0])
    return pairs


# ==========================================================
# Main
# ==========================================================

def main():
    all_series = []  # list of (legend, xs, ys)
    for i, d in enumerate(TARGET_DIRS):
        legend = LEGEND_LABELS[i] if i < len(LEGEND_LABELS) else os.path.basename(d.rstrip("/"))
        file_path = d

        if not os.path.exists(file_path):
            print(f"Warning: File not found -> {file_path}")
            all_series.append((legend, [], []))
            continue

        with open(file_path, "r") as f:
            file_data = json.load(f)

        pairs = extract_sweep_pairs(file_data, X_PARAM, Y_PARAM)
        xs = [p[0] for p in pairs]
        ys = [p[1] for p in pairs]
        all_series.append((legend, xs, ys))
        print(f"[{legend}] {len(pairs):>4} points  <- {file_path}")

    # ---------- Auto-scale axes ----------
    all_x = [v for _, xs, _ in all_series for v in xs]
    all_y = [v for _, _, ys in all_series for v in ys]

    x_scale, x_prefix = auto_scale(all_x)
    y_scale, y_prefix = auto_scale(all_y)

    # ---------- Plot: one curve per temperature ----------
    fig, ax = plt.subplots(figsize=(12, 7))

    for i, (legend, xs, ys) in enumerate(all_series):
        if not xs:
            continue
        color = COLORS[i % len(COLORS)]
        xs_s = [x * x_scale for x in xs]
        ys_s = [y * y_scale for y in ys]
        ax.plot(
            xs_s, ys_s,
            marker="o", markersize=3.5, linewidth=1.6,
            color=color, label=legend, alpha=0.9,
        )

    ax.set_xlabel(format_label(X_PARAM, x_prefix, X_UNIT),
                  fontweight="bold", fontsize=11)
    ax.set_ylabel(format_label(Y_PARAM, y_prefix, Y_UNIT),
                  fontweight="bold", fontsize=11)
    ax.set_title(f"{Y_PARAM} vs {X_PARAM} across temperatures",
                 fontweight="bold", fontsize=14, color="#333333")

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.set_axisbelow(True)
    ax.grid(True, linestyle="--", alpha=0.5)

    ax.legend(
        loc="best", frameon=True, framealpha=0.9,
        fontsize=9, ncol=2, title="Temperature",
    )

    plt.tight_layout()
    plt.savefig(OUTPUT_FILE, dpi=300, bbox_inches="tight")
    plt.show()
    print(f"Saved: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
