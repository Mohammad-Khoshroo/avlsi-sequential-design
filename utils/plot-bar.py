import os
import json
import numpy as np
import matplotlib.pyplot as plt

TARGET_DIRS = [
    r"./simulation/BKA/corners/FF/power/",
    r"./simulation/BKA/corners/FS/power/",
    r"./simulation/BKA/corners/SF/power/",
    r"./simulation/BKA/corners/SS/power/",
    r"./simulation/BKA/corners/TT/power/"
]

PARAM_KEYS = ["p_avg", "p_static_avg",  "p_dynamic_avg","p_max", "p_static_max",  "p_dynamic_max"]
PARAM_LABELS = ["p_total", "p_static",  "p_dynamic","p_peak", "p_static_peak",  "p_dynamic_peak"]

PARAM_PATHS = [key for key in PARAM_KEYS]

COLORS = [
    "#636EFA",
    "#EF553B",
    "#00CC96",
    "#AB63FA",
    "#FFA15A",
    "#19D3F3",
    "#FF6692",
    "#B6E880",
    "#FF97FF",
    "#FECB52",
]


def get_nested_value(data_dict, path_list):
    temp = data_dict
    for key in path_list:
        if isinstance(temp, dict) and key in temp:
            temp = temp[key]
        else:
            return 0.0
    return float(temp)


raw_extracted_data = {}

for d in TARGET_DIRS:
    parts = [p for p in d.split("/") if p]
    arch_name = parts[-2] if len(parts) >= 2 else d

    file_path = os.path.join(d, "measure.json")

    data_points = []
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            file_data = json.load(f)

        for path in PARAM_PATHS:
            val = get_nested_value(file_data, [path])
            data_points.append(val)
    else:
        print(f"Warning: File not found -> {file_path}")
        data_points = [0.0] * len(PARAM_LABELS)

    raw_extracted_data[arch_name] = data_points

all_non_zero_values = []
for vals in raw_extracted_data.values():
    for v in vals:
        if abs(v) > 1e-20:  
            all_non_zero_values.append(abs(v))

if not all_non_zero_values:
    scale_factor = 1.0
    unit_prefix = ""
else:
    mean_exponent = np.mean([int(np.floor(np.log10(v))) for v in all_non_zero_values])
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

si_extracted_data = {}
for arch, values in raw_extracted_data.items():
    si_extracted_data[arch] = [v * scale_factor for v in values]

num_params = len(PARAM_LABELS)
max_val_per_param = []

for p_idx in range(num_params):
    vals_for_this_param = [si_extracted_data[arch][p_idx] for arch in si_extracted_data]
    max_val_per_param.append(max(vals_for_this_param) if vals_for_this_param else 0.0)

global_max = max(max_val_per_param) if max_val_per_param else 1.0

param_boost_factors = []
param_alphas = []

for p_idx in range(num_params):
    max_val = max_val_per_param[p_idx]
    if max_val > 1e-15:
        ratio = max_val / global_max
        
        diff = int(np.ceil(-np.log10(ratio))) if ratio < 1.0 else 0
        
        if diff >= 2:
            boost = 10 ** (diff - 1)
            alpha = 0.45
        else:
            boost = 1.0
            alpha = 1.0
    else:
        boost = 1.0
        alpha = 1.0
        
    param_boost_factors.append(boost)
    param_alphas.append(alpha)

visual_data = {}
original_text_labels = {}

for arch, values in si_extracted_data.items():
    v_list = []
    t_list = []
    for p_idx, v in enumerate(values):
        boost = param_boost_factors[p_idx]
        v_list.append(v * boost)
        t_list.append(f"{v:.2f}" if v > 1e-15 else "0.00")
    visual_data[arch] = v_list
    original_text_labels[arch] = t_list


fig, ax = plt.subplots(figsize=(12, 6))

x = np.arange(len(PARAM_LABELS))
num_archs = len(visual_data)
width = 0.8 / num_archs if num_archs > 0 else 0.8

for i, (arch_name, values) in enumerate(visual_data.items()):
    x_offset = x + (i - num_archs / 2 + 0.5) * width
    labels_to_show = original_text_labels[arch_name]

    for j in range(len(values)):
        rect = ax.bar(
            x_offset[j],
            values[j],
            width,
            color=COLORS[i % len(COLORS)],
            edgecolor="black",
            linewidth=0.5,
            alpha=param_alphas[j],
            label=arch_name if j == 0 else ""
        )
        ax.bar_label(rect, labels=[labels_to_show[j]], padding=3, fontsize=8, rotation=45)

ax.set_ylabel(f"power({unit_prefix})", fontweight="bold", fontsize=11)
ax.set_title("Parameters Comparison", fontweight="bold", fontsize=14, pad=15)
ax.set_xticks(x)
ax.set_xticklabels(PARAM_LABELS, fontweight="bold", fontsize=10)
ax.legend(title="Architectures", frameon=True)

ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

ax.set_axisbelow(True)
ax.yaxis.grid(True, linestyle="--", alpha=0.7)

current_ylim = ax.get_ylim()
ax.set_ylim(current_ylim[0], current_ylim[1] * 1.2)

plt.tight_layout()
plt.savefig("styled_bar_plot.png", dpi=300)
plt.show()