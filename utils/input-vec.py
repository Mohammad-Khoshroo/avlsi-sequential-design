import itertools
import re

INPUT_DEFS = {"A": 8, "B": 8, "Cin": 1}
OUTPUT_DEFS = {"S": 8, "Cout": 1}
LOGIC = {"S": "A + B + Cin", "Cout": "(A + B + Cin) >> 8"}

VEC_SETTINGS = {
    "tunit": "ns",
    "trise": "0.1n",
    "tfall": "0.1n",
    "vih": 1.8,
    "vil": 0,
    "voh": 1.8,
    "vol": 0,
    "tp": 5,      
    "period": 10  
}

OUTPUT_VEC_PATH = "input.vec"

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

def generate_data():
    compiled_logic = {
        out_name: translate_verilog_to_python(expr) for out_name, expr in LOGIC.items()
    }

    total_in_bits = sum(INPUT_DEFS.values())
    combinations = list(itertools.product([0, 1], repeat=total_in_bits))
    
    results = []
    
    for combo in combinations:
        current_idx = 0
        input_vals = {}
        for name, bits in INPUT_DEFS.items():
            var_bits = combo[current_idx : current_idx + bits]
            input_vals[name] = int("".join(map(str, var_bits)), 2)
            current_idx += bits

        out_dict = {}
        for name, bits in OUTPUT_DEFS.items():
            val = eval(compiled_logic[name], {}, input_vals)
            val = val & ((1 << bits) - 1)
            out_dict[name] = format(val, f"0{bits}b")

        in_str = "".join(map(str, combo))
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

if __name__ == "__main__":
    print("Step 1: Calculating Logic and Truth Table...")
    table_data = generate_data()
    
    print(f"Step 2: Generating VEC file with {len(table_data)} vectors...")
    create_vec_file(table_data)
    
    print(f"Successfully finished! File saved as '{OUTPUT_VEC_PATH}'.")
