import json
import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# =====================================================================
# File Paths and Target Parameters Setup
# =====================================================================
CSV_FILE_PATH = "./simulation/BKA/mont-carlo/sim.tail0.csv"  # Path to HSPICE data file
JSON_FILE_PATH = "./simulation/BKA/mont-carlo/vdd_val.json"  # Path to JSON file (list of dicts)

TARGET_MEASURES = ["p_max", "p_avg", "tp_max", "tp_avg", "vdd_actual"]


def parse_hspice_tail_with_indices(csv_path, json_path):
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"Data file not found at path: {csv_path}!")

    # Load JSON file
    var_mapping = {}
    if os.path.exists(json_path):
        with open(json_path, "r", encoding="utf-8") as jf:
            raw_json = json.load(jf)
            for item in raw_json:
                idx = item.get("index")
                val = item.get("vdd_val")
                if idx is not None:
                    var_mapping[str(idx)] = val
        print(
            f"JSON file loaded successfully. {len(var_mapping)} variables read."
        )
    else:
        print(
            "Warning: JSON file not found. Plots will be drawn with raw index numbers."
        )

    measure_names = []
    left_tail_data = []
    right_tail_data = []
    left_indices = []
    right_indices = []

    current_section = None

    with open(csv_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            # Identify file sections
            if line.startswith("#Measure names"):
                current_section = "names"
                continue
            elif line.startswith("#Measure values in left tail"):
                current_section = "left_vals"
                continue
            elif line.startswith("#Measure values in right tail"):
                current_section = "right_vals"
                continue
            elif line.startswith("#Index values in left tail"):
                current_section = "left_idx"
                continue
            elif line.startswith("#Index values in right tail"):
                current_section = "right_idx"
                continue

            # Extract data based on current section
            if current_section == "names":
                measure_names = line.split(",")
            elif current_section == "left_vals":
                row = [float(val) for val in line.split(",")]
                left_tail_data.append(row)
            elif current_section == "right_vals":
                row = [float(val) for val in line.split(",")]
                right_tail_data.append(row)
            elif current_section == "left_idx":
                row = [int(val) for val in line.split(",")]
                left_indices.append(row)
            elif current_section == "right_idx":
                row = [int(val) for val in line.split(",")]
                right_indices.append(row)

    # Convert to DataFrames
    df_left_val = pd.DataFrame(left_tail_data, columns=measure_names)
    df_right_val = pd.DataFrame(right_tail_data, columns=measure_names)

    df_left_idx = pd.DataFrame(left_indices, columns=measure_names)
    df_right_idx = pd.DataFrame(right_indices, columns=measure_names)

    return measure_names, df_left_val, df_right_val, df_left_idx, df_right_idx, var_mapping


def plot_tails_with_variable_labels(
    measure_names, df_l, df_r, df_l_idx, df_r_idx, var_map, target_measures
):
    # If target list is empty, plot all available measures
    if not target_measures:
        selected_measures = measure_names
    else:
        # Select only measures that exist in both the file and target list
        selected_measures = [m for m in target_measures if m in measure_names]
        ignored = [m for m in target_measures if m not in measure_names]
        if ignored:
            print(f"Warning: The following measures were not found in the file and will not be plotted: {ignored}")

    num_measures = len(selected_measures)
    if num_measures == 0:
        print("No valid measures found for plotting!")
        return

    # Optimize number of rows and columns for subplots
    cols = min(3, num_measures)
    rows = int(np.ceil(num_measures / cols))

    fig, axes = plt.subplots(rows, cols, figsize=(5 * cols, rows * 4.8))
    
    # If only one plot, convert axes to an array to prevent errors
    if num_measures == 1:
        axes = np.array([axes])
    else:
        axes = axes.flatten()

    for i, col_name in enumerate(selected_measures):
        ax = axes[i]

        left_vals = df_l[col_name].values
        right_vals = df_r[col_name].values

        left_idx_list = df_l_idx[col_name].values
        right_idx_list = df_r_idx[col_name].values

        def get_label(idx):
            val_from_json = var_map.get(str(idx), None)
            if val_from_json is not None:
                return f"Idx:{idx} ({val_from_json})"
            return f"Idx:{idx}"

        x_indices = np.arange(len(left_vals))

        ax.plot(
            x_indices,
            left_vals,
            marker="o",
            linestyle="-",
            color="blue",
            label="Left Tail (Min)",
        )
        ax.plot(
            x_indices,
            right_vals,
            marker="s",
            linestyle="-",
            color="red",
            label="Right Tail (Max)",
        )

        combined_labels = []
        for j in range(len(x_indices)):
            l_lbl = get_label(left_idx_list[j])
            r_lbl = get_label(right_idx_list[j])
            combined_labels.append(f"L: {l_lbl}\nR: {r_lbl}")

        ax.set_xticks(x_indices)
        ax.set_xticklabels(combined_labels, fontsize=8, rotation=45, ha="right")

        ax.set_title(col_name, fontsize=11, fontweight="bold")
        ax.grid(True, linestyle="--", alpha=0.5)

        if i == 0:
            ax.legend()

    # Remove extra empty subplots
    for j in range(i + 1, len(axes)):
        fig.delaxes(axes[j])

    plt.tight_layout()
    plt.savefig("combined_subplots_plot.png", dpi=300, bbox_inches="tight")
    plt.show()


# =====================================================================
# Main Process Execution
# =====================================================================
if __name__ == "__main__":
    try:
        print("Starting file analysis...")
        (
            measures,
            df_l_val,
            df_r_val,
            df_l_idx,
            df_r_idx,
            var_map,
        ) = parse_hspice_tail_with_indices(CSV_FILE_PATH, JSON_FILE_PATH)

        print("Plotting graphs...")
        plot_tails_with_variable_labels(
            measures, df_l_val, df_r_val, df_l_idx, df_r_idx, var_map, TARGET_MEASURES
        )

    except Exception as e:
        import traceback

        print(f"An error occurred: {e}")
        traceback.print_exc()
