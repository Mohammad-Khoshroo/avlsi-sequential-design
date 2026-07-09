import json

file_path = "./simulation/BKA/corners/TT/power/static/measure.json"


def analyze_static_power(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        measurements = data.get("measurements", {})
        if not measurements:
            print("NOT FOUND ANYTHING")
            return

        values = list(measurements.values())

        avg_value = sum(values) / len(values)
        max_value = max(values)

        data["summary"] = {"avg": avg_value, "max": max_value}

        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

        print(
            "DONE"
        )

    except FileNotFoundError:
        print(f"file not found")
    except json.JSONDecodeError:
        print("Is's not json")


analyze_static_power(file_path)
