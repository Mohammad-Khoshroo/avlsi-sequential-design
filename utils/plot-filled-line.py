import os
import json
import numpy as np
import matplotlib.pyplot as plt

TARGET_DIRS = [
    r"./simulation/BKA/temperature/Sim_Results/Temp15/",
    r"./simulation/BKA/temperature/Sim_Results/Temp20/",
    r"./simulation/BKA/temperature/Sim_Results/Temp25/",
    r"./simulation/BKA/temperature/Sim_Results/Temp30/",
    r"./simulation/BKA/temperature/Sim_Results/Temp35/",
    r"./simulation/BKA/temperature/Sim_Results/Temp40/",
    r"./simulation/BKA/temperature/Sim_Results/Temp45/",
    r"./simulation/BKA/temperature/Sim_Results/Temp50/",
    r"./simulation/BKA/temperature/Sim_Results/Temp55/",
    r"./simulation/BKA/temperature/Sim_Results/Temp60/",
    r"./simulation/BKA/temperature/Sim_Results/Temp65/",
    r"./simulation/BKA/temperature/Sim_Results/Temp70/",
    r"./simulation/BKA/temperature/Sim_Results/Temp75/",
    r"./simulation/BKA/temperature/Sim_Results/Temp80/",
    r"./simulation/BKA/temperature/Sim_Results/Temp85/",
    r"./simulation/BKA/temperature/Sim_Results/Temp90/",
]

X_AXIS_LABELS = [
    "15°C",
    "20°C",
    "25°C",
    "30°C",
    "35°C",
    "40°C",
    "45°C",
    "50°C",
    "55°C",
    "60°C",
    "65°C",
    "70°C",
    "75°C",
    "80°C",
    "85°C",
    "90°C",
]

PARAM_LABELS = ["p_max", "p_avg"]

PARAM_PATHS = [
    # ["1", "measurements", "tp_cout"],
    # ["1", "measurements", "tp_s8"],
    ["1", "measurements", "p_max"],
    ["1", "measurements", "p_avg"]
]

COLORS = [
    "#636EFA",
    "#EF553B",
    "#00CC96",
    "#AB63FA",
    "#FFA15A",
]


def get_nested_value(data_dict, path_list):
    temp = data_dict
    for key in path_list:
        if isinstance(temp, dict) and key in temp:
            temp = temp[key]
        else:
            return 0.0
    return float(temp)


x_labels = []
raw_data_matrix = {key: [] for key in PARAM_LABELS}

for i, d in enumerate(TARGET_DIRS):
    if i < len(X_AXIS_LABELS):
        corner_name = X_AXIS_LABELS[i]
    else:
        parts = [p for p in d.split("/") if p]
        corner_name = parts[-1] if len(parts) >= 1 else d

    x_labels.append(corner_name)

    file_path = os.path.join(d, "measure.json")

    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            file_data = json.load(f)
        for path, key in zip(PARAM_PATHS, PARAM_LABELS):
            val = get_nested_value(file_data, path)
            raw_data_matrix[key].append(val)
    else:
        print(f"Warning: File not found -> {file_path}")
        for key in PARAM_LABELS:
            raw_data_matrix[key].append(0.0)

all_values = [v for vals in raw_data_matrix.values() for v in vals if abs(v) > 1e-20]

if not all_values:
    scale_factor = 1.0
    unit_prefix = ""
else:
    mean_exponent = np.mean([int(np.floor(np.log10(v))) for v in all_values])
    if mean_exponent < -10:
        scale_factor = 1e12
        unit_prefix = "p"
    elif mean_exponent < -7:
        scale_factor = 1e9
        unit_prefix = "n"
    elif mean_exponent < -4:
        scale_factor = 1e6
        unit_prefix = "u"
    elif mean_exponent < -1:
        scale_factor = 1e3
        unit_prefix = "m"
    else:
        scale_factor = 1.0
        unit_prefix = ""

scaled_data_matrix = {
    key: [v * scale_factor for v in raw_data_matrix[key]] for key in PARAM_LABELS
}


n_params = len(PARAM_LABELS)
ncols = 2
nrows = int(np.ceil(n_params / ncols)) 

height_per_row = 4.5
fig_height = max(5, nrows * height_per_row)

fig, axes = plt.subplots(nrows=nrows, ncols=ncols, figsize=(16, fig_height))

if nrows == 1:
    axes_flat = axes
else:
    axes_flat = axes.flatten()


x_indices = np.arange(len(x_labels))

for idx, key in enumerate(PARAM_LABELS):
    ax = axes_flat[idx]
    y_values = scaled_data_matrix[key]
    color = COLORS[idx % len(COLORS)]

    ax.plot(x_indices, y_values, marker="o", linewidth=2, color=color, label=key)

    ax.fill_between(x_indices, y_values, color=color, alpha=0.1)

    for xi, yi in zip(x_indices, y_values):
        ax.text(
            xi,
            yi,
            f"{yi:.2f}",
            fontsize=7,
            ha="center",
            va="bottom",
            fontweight="semibold",
            rotation=30,
        )

    ax.set_title(f"{key}", fontweight="bold", fontsize=11, color="#333333")
    ax.set_ylabel(f"Delay ({unit_prefix}s)", fontweight="bold", fontsize=9)
    ax.set_xticks(x_indices)
    ax.set_xticklabels(x_labels, fontweight="bold", fontsize=8, rotation=45)

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    ax.set_axisbelow(True)
    ax.grid(True, linestyle="--", alpha=0.5)

    if y_values:
        y_min = min(y_values)
        y_max = max(y_values)
        y_range = y_max - y_min
        if y_range < 1e-9:
            ax.set_ylim(y_min * 0.9, y_max * 1.3)
        else:
            ax.set_ylim(y_min - 0.05 * y_range, y_max + 0.3 * y_range)

if len(axes_flat) > n_params:
    for empty_idx in range(n_params, len(axes_flat)):
        fig.delaxes(axes_flat[empty_idx])

plt.suptitle(
    "Parameters Comparison",
    fontweight="bold",
    fontsize=16,
    y=0.98,
)
plt.tight_layout()

plt.savefig("combined_subplots_plot.png", dpi=300, bbox_inches="tight")
plt.show()
