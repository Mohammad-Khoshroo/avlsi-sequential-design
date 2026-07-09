import json
import os

TARGET_DIRS = [
    r"./simulation/BKA/corners/FF/power/",
    r"./simulation/BKA/corners/FS/power/",
    r"./simulation/BKA/corners/SF/power/",
    r"./simulation/BKA/corners/SS/power/",
    r"./simulation/BKA/corners/TT/power/",
]

for d in TARGET_DIRS:
    file_path = os.path.join(d, "measure.json")

    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            data = json.load(f)

        p_avg = data.get("p_avg", 0.0)
        p_max = data.get("p_max", 0.0)
        p_static_avg = data.get("p_static_avg", 0.0)
        p_static_max = data.get("p_static_max", 0.0)

        data["p_dynamic_avg"] = p_avg - p_static_avg
        data["p_dynamic_max"] = p_max - p_static_max

        with open(file_path, "w") as f:
            json.dump(data, f, indent=4)

        print(f"Updated successfully: {file_path}")
    else:
        print(f"Warning: File not found -> {file_path}")
