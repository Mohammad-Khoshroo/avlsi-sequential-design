import json
import os

# ==========================================
# CONFIGURATION
# ==========================================
# 1. Define your input file path here:
FILE_PATH = r"./simulation/BKA/mont-carlo/sim.mc0"  # Supports any extension (e.g., .lis, .txt, .tr0)

# 2. Define the nominal supply voltage (nominal Vdd):
NOMINAL_VDD = 1.0  # Change this to match your nominal supply (e.g., 1.0, 1.2, etc.)

# 3. Define the standard deviation (sigma) value:
STD_DEV = 0.1  # Matches your .PARAM dev=agauss(0, 0.1)
# ==========================================


def parse_hspice_data(file_path, nominal_vdd, std_dev):
    data = []
    headers = []
    header_found = False

    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()

            # Skip empty lines, comments, and HSPICE configuration options
            if not line or line.startswith("$") or line.startswith("."):
                continue

            # Identify the header line (starts with "index")
            if line.lower().startswith("index"):
                raw_headers = line.split()
                headers = []
                for h in raw_headers:
                    # Clean headers from extra strings like ':@:dev:@:IGNC'
                    clean_h = h.split(":@:")[0]
                    headers.append(clean_h)
                header_found = True
                continue

            # Extract data values after the header has been identified
            if header_found:
                parts = line.split()
                if len(parts) == len(headers):
                    row_dict = {}
                    for col, val in zip(headers, parts):
                        try:
                            if col.lower() == "index":
                                # Keep index as an integer
                                row_dict[col] = int(val)
                            else:
                                # Calculate the actual voltage: Vdd_actual = Nominal_Vdd + (Normalized_Val * Std_Dev)
                                normalized_val = float(val)
                                actual_val = nominal_vdd + (normalized_val * std_dev)
                                row_dict[col] = actual_val
                        except ValueError:
                            row_dict[col] = val  # Keep as string if conversion fails
                    data.append(row_dict)

    return data


def main():
    if not os.path.exists(FILE_PATH):
        print(f"Error: File not found at specified path: {FILE_PATH}")
        return

    # Extract directory and filename to save the output JSON in the same directory
    directory, filename = os.path.split(FILE_PATH)
    name_without_ext, _ = os.path.splitext(filename)

    json_filename = f"{name_without_ext}.json"
    json_path = os.path.join(directory, json_filename)

    print(f"Processing file...")
    print(f"Formula: Actual Vdd = {NOMINAL_VDD} + (Value * {STD_DEV})")
    
    parsed_data = parse_hspice_data(FILE_PATH, NOMINAL_VDD, STD_DEV)

    if not parsed_data:
        print("Error: No data extracted from the file.")
        return

    print(f"Saving JSON to: {json_path}")
    with open(json_path, "w", encoding="utf-8") as json_file:
        json.dump(parsed_data, json_file, indent=4, ensure_ascii=False)

    print("Success: File successfully converted to JSON with actual Vdd values!")


if __name__ == "__main__":
    main()
