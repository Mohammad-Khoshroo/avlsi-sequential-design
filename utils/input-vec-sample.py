import random
import re

INPUT_DEFS = {"A": 8, "B": 8, "Cin": 1}
OUTPUT_DEFS = {"S": 8, "Cout": 1}
LOGIC = {"S": "A + B + Cin", "Cout": "(A + B + Cin) >> 8"}

VEC_SETTINGS = {
    "tunit": "ps",
    "trise": "50",
    "tfall": "50",
    "vih": 1,
    "vil": 0,
    "voh": 0.95,
    "vol": 0.01,
    "tp": 1000,
    "period": 1300
}

OUTPUT_VEC_PATH = "input.vec"
OUTPUT_MEAS_PATH = "static_measures.sp"
NUM_RANDOM_VECTORS = 1000

def translate_verilog_to_python(expr):
    def replace_slice(m):
        var, msb, lsb = m.group(1), int(m.group(2)), int(m.group(3))
        mask = (1 << (msb - lsb + 1)) - 1
        return f"(({var} >> {lsb}) & {mask})"

    def replace_bit(m):
        var, bit = m.group(1), m.group(2)
        return f"(({var} >> {bit}) & 1)"

    expr = re.sub(r"([a-zA-Z_]\w*)\[(\d+):(\d+)\]", replace_slice, expr)
    expr = re.sub(r"([a-zA-Z_]\w*)\[(\d+)\]", replace_bit, expr)
    return expr

def generate_data(num_vectors):
    compiled_logic = {
        out_name: translate_verilog_to_python(expr) for out_name, expr in LOGIC.items()
    }

    results = []

    for _ in range(num_vectors):
        input_vals = {}
        in_str_parts = []

        for name, bits in INPUT_DEFS.items():
            val = random.randint(0, (1 << bits) - 1)
            input_vals[name] = val
            in_str_parts.append(format(val, f"0{bits}b"))

        out_dict = {}
        for name, bits in OUTPUT_DEFS.items():
            val = eval(compiled_logic[name], {}, input_vals)
            val = val & ((1 << bits) - 1)
            out_dict[name] = format(val, f"0{bits}b")

        in_str = "".join(in_str_parts)
        out_str = "".join(out_dict.values())
        results.append((in_str, out_str))

    return results

def create_vec_file(truth_table):
    vnames = []
    ios = []
    radixes = []

    for pin, width in INPUT_DEFS.items():
        vnames.append(pin if width == 1 else f"{pin}[{width-1}:0]")
        ios.extend(['i'] * width)
        radixes.extend(['1'] * width)

    for pin, width in OUTPUT_DEFS.items():
        vnames.append(pin if width == 1 else f"{pin}[{width-1}:0]")
        ios.extend(['o'] * width)
        radixes.extend(['1'] * width)

    with open(OUTPUT_VEC_PATH, 'w') as f:
        f.write(f"radix {' '.join(radixes)}\n")
        f.write(f"vname {' '.join(vnames)}\n")
        f.write(f"io {' '.join(ios)}\n")
        for key in ['tunit', 'trise', 'tfall', 'vih', 'vil', 'voh', 'vol']:
            f.write(f"{key} {VEC_SETTINGS[key]}\n")
        f.write("\n")

        current_time = 0
        tp = VEC_SETTINGS['tp']
        period = VEC_SETTINGS['period']

        out_x_str = ' '.join(['X' * width for width in OUTPUT_DEFS.values()])

        for in_bits, out_bits in truth_table:
            in_list = []
            idx = 0
            for width in INPUT_DEFS.values():
                in_list.append(in_bits[idx:idx+width])
                idx += width
            in_val_str = ' '.join(in_list)

            out_list = []
            idx = 0
            for width in OUTPUT_DEFS.values():
                out_list.append(out_bits[idx:idx+width])
                idx += width
            out_val_str = ' '.join(out_list)

            f.write(f"{current_time} {in_val_str} {out_x_str}\n")
            f.write(f"{current_time + tp} {in_val_str} {out_val_str}\n")

            current_time += period

def create_static_measure_file(num_vectors):
    tp = VEC_SETTINGS['tp']
    period = VEC_SETTINGS['period']
    tunit = VEC_SETTINGS['tunit']
    
    with open(OUTPUT_MEAS_PATH, 'w') as f:
        f.write("* --- HSPICE Static Power Measurements for each vector ---\n")
        f.write(f"* Total Vectors: {num_vectors}\n\n")

        for i in range(num_vectors):
            t_start_period = i * period
            t_stable_start = t_start_period + tp
            t_stable_end = t_start_period + period
            
            f.write(
                f".MEASURE TRAN P_static_{i} AVG POWER "
                f"FROM={t_stable_start}{tunit} TO={t_stable_end}{tunit}\n"
            )
        
        f.write("\n* --------------------------------------------------------\n")

if __name__ == "__main__":
    print("Step 1: Generating random input vectors and calculating outputs...")
    table_data = generate_data(NUM_RANDOM_VECTORS)

    print(f"Step 2: Generating VEC file with {len(table_data)} random vectors...")
    create_vec_file(table_data)

    print(f"Step 3: Generating HSPICE measurement file for static power...")
    create_static_measure_file(NUM_RANDOM_VECTORS)

    print(f"Successfully finished! Files saved:\n- Vector file: '{OUTPUT_VEC_PATH}'\n- Measure file: '{OUTPUT_MEAS_PATH}'")
