import os
import json
import numpy as np
import matplotlib.pyplot as plt

TARGET_DIRS = [
    r"./simulation/RCA/corners/TT/delay/",
    r"./simulation/BKA/corners/TT/delay/",
    # r"./simulation/FA/nand-based/delay/",
    # r"./simulation/FA/mirror/delay/",
    # r"./simulation/FA/TG-based/delay/",
]

DIR_LABELS = ["RCA", "BKA"]

PARAM_PATHS = [
    ["measurements", "tp_max"],                 
    ["measurements", "tp_cout"],               
    ["measurements", "tp_s8"],          
    ["measurements", "p_avg"],       
    ["measurements", "p_max"],
    ["measurements", "area"],                              
]

PARAM_LABELS = ["tp(max)", "tp(cout)", "tp(sum)", "power(avg)", "power(max)", "area"]

COLORS = ['#636EFA', '#EF553B', '#00CC96', '#AB63FA']

def get_nested_value(data_dict, path_list):
    temp = data_dict
    for key in path_list:
        if isinstance(temp, dict) and key in temp:
            temp = temp[key]
        else:
            return 0.0
    return float(temp)

raw_data = {d: [] for d in TARGET_DIRS}

for d in TARGET_DIRS:
    file_path = os.path.join(d, "measure.json") 
    
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            file_data = json.load(f)
        
        for path in PARAM_PATHS:
            val = get_nested_value(file_data, path)
            raw_data[d].append(val)
    else:
        print(f"Warning: File not found -> {file_path}")
        raw_data[d] = [0.0] * len(PARAM_PATHS)

raw_matrix = np.array([raw_data[d] for d in TARGET_DIRS])

max_vals = np.max(raw_matrix, axis=0)
max_vals[max_vals == 0] = 1.0

normalized_data = {}
for i, d in enumerate(TARGET_DIRS):
    normalized_data[d] = raw_matrix[i] / max_vals

num_vars = len(PARAM_LABELS)
angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()

angles += angles[:1]

fig, ax = plt.subplots(figsize=(9, 9), subplot_kw=dict(polar=True))

for i, d in enumerate(TARGET_DIRS):
    values = normalized_data[d].tolist()
    values_closed = values + values[:1]
    
    ax.plot(angles, values_closed, color=COLORS[i % len(COLORS)], linewidth=2, label=DIR_LABELS[i])
    ax.fill(angles, values_closed, color=COLORS[i % len(COLORS)], alpha=0.15)

ax.set_theta_offset(np.pi / 2)
ax.set_theta_direction(-1)    


ax.set_xticks(angles[:-1])
ax.set_xticklabels(PARAM_LABELS, fontweight='bold', fontsize=11)

ax.set_ylim(0, 1.05)
ax.set_rgrids([0.2, 0.4, 0.6, 0.8, 1.0], labels=['20%', '40%', '60%', '80%', '100%'], color='grey', size=9)

ax.yaxis.grid(True, color='#E0E0E0', linestyle='--', linewidth=0.8)
ax.xaxis.grid(True, color='#B0B0B0', linestyle='-', linewidth=0.8)

plt.title('Full Adder Architectures Comparison', fontweight='bold', fontsize=13, pad=30)
plt.legend(loc='upper right', bbox_to_anchor=(1.2, 1.1), fontsize=10)

plt.tight_layout()

plt.savefig('radar_chart_normalized.png', dpi=300, bbox_inches='tight')
plt.show()
