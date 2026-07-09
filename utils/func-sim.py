def generate_spice_deck():
    print("=== SPICE Timing & Delay Generator (Multi-Output, Separated LH/HL) ===")
    
    # 1. Get the number of INPUT signals
    while True:
        try:
            n = int(input("Enter the number of INPUT signals (n) (e.g., 2 or 3): "))
            if n > 0: break
        except ValueError:
            print("Please enter a valid integer.")

    # 2. Get the names of the INPUT signals
    signals = []
    for i in range(n):
        sig = input(f"Enter the name of INPUT signal {i+1} (e.g., A, B, Cin): ").strip()
        signals.append(sig)

    # 3. Get the number of OUTPUT signals
    while True:
        try:
            m = int(input("Enter the number of OUTPUT signals (e.g., 1 or 2): "))
            if m > 0: break
        except ValueError:
            print("Please enter a valid integer.")

    # 4. Get the names of the OUTPUT signals
    outputs = []
    for i in range(m):
        out_sig = input(f"Enter the name of OUTPUT signal {i+1} (e.g., S, Cout): ").strip()
        outputs.append(out_sig)

    # 5. Get the time window duration
    while True:
        try:
            w_input = input("Enter the duration of each time window in picoseconds (e.g., 800): ")
            W = float(w_input)
            if W > 0: break
        except ValueError:
            print("Please enter a valid number.")

    # Relative timing settings
    t_r = 0.05 * W         
    t_d1 = 0.25 * W        
    t_d2 = 0.65 * W        
    
    meas1_from = 0.10 * W  
    meas1_to = 0.45 * W    
    meas2_from = 0.50 * W  
    meas2_to = 0.90 * W    

    # PWL GENERATION LOGIC (State Machine)
    def val_str(state):
        return "'Vdd_val'" if state == 1 else "0"

    pwl_points = {sig: [(0.0, "0")] for sig in signals}
    current_state = {sig: 0 for sig in signals}
    
    tests_info = []
    test_idx = 1
    
    for toggle_idx in range(n):
        toggle_sig = signals[toggle_idx]
        other_sigs = signals[:toggle_idx] + signals[toggle_idx+1:]
        num_combinations = 2 ** (n - 1)
        
        for b in range(num_combinations):
            T_S = (test_idx - 1) * W
            T_E = test_idx * W
            
            static_states = {}
            for bit_idx, other_sig in enumerate(other_sigs):
                state = (b >> bit_idx) & 1
                static_states[other_sig] = state

            for sig in signals:
                if sig == toggle_sig:
                    if current_state[sig] != 0:
                        pwl_points[sig].append((T_S, val_str(current_state[sig])))
                        pwl_points[sig].append((T_S + t_r, val_str(0)))
                        current_state[sig] = 0
                    
                    pwl_points[sig].append((T_S + t_d1, val_str(0)))
                    pwl_points[sig].append((T_S + t_d1 + t_r, val_str(1)))
                    pwl_points[sig].append((T_S + t_d2, val_str(1)))
                    pwl_points[sig].append((T_S + t_d2 + t_r, val_str(0)))
                    current_state[sig] = 0
                else:
                    target = static_states[sig]
                    if current_state[sig] != target:
                        pwl_points[sig].append((T_S, val_str(current_state[sig])))
                        pwl_points[sig].append((T_S + t_r, val_str(target)))
                        current_state[sig] = target

            tests_info.append({
                'id': test_idx,
                'T_S': T_S,
                'T_E': T_E,
                'toggle': toggle_sig,
                'statics': static_states
            })
            test_idx += 1

    Final_T = (test_idx - 1) * W
    for sig in signals:
        pwl_points[sig].append((Final_T, val_str(current_state[sig])))

    # Helper function for Cascaded MAX (Without DEFAULT)
    def write_cascaded_max(f_obj, meas_list, final_name):
        if not meas_list:
            return
        if len(meas_list) == 1:
            f_obj.write(f".MEASURE TRAN {final_name} PARAM='{meas_list[0]}'\n")
        elif len(meas_list) == 2:
            f_obj.write(f".MEASURE TRAN {final_name} PARAM='MAX({meas_list[0]}, {meas_list[1]})'\n")
        else:
            f_obj.write(f".MEASURE TRAN {final_name}_m1 PARAM='MAX({meas_list[0]}, {meas_list[1]})'\n")
            for i in range(2, len(meas_list) - 1):
                f_obj.write(f".MEASURE TRAN {final_name}_m{i} PARAM='MAX({final_name}_m{i-1}, {meas_list[i]})'\n")
            last_idx = len(meas_list) - 2
            f_obj.write(f".MEASURE TRAN {final_name} PARAM='MAX({final_name}_m{last_idx}, {meas_list[-1]})'\n")

    # ================= Write to File =================
    def fmt_num(num):
        return f"{int(num)}" if float(num).is_integer() else f"{num}"

    filename = "timing-test.sp"
    
    with open(filename, "w") as f:
        f.write("* ===================================================================\n")
        f.write("* Timing & Delay\n\n")

        # Write Input PWLs
        for sig in signals:
            points_str = "  ".join([f"{fmt_num(t)}p {v}" for t, v in pwl_points[sig]])
            f.write(f"V{sig} {sig} 0 PWL({points_str})\n")
        
        f.write("\n")
        
        # Store separate LH and HL measurements per output
        all_LH_meas = {out: [] for out in outputs}
        all_HL_meas = {out: [] for out in outputs}

        for test in tests_info:
            T_S = test['T_S']
            T_E = test['T_E']
            toggle = test['toggle']
            statics = test['statics']
            test_id = test['id']

            stat_str_list = [f"{k}={v}" for k, v in statics.items()]
            stat_str = ", ".join(stat_str_list) if stat_str_list else "All pins toggle"
            
            # Clean names for measure variable creation
            short_toggle = toggle.replace('in', '')
            short_statics = "".join([f"{k.replace('in', '')}{v}" for k, v in statics.items()])

            f.write("* -------------------------------------------------------------------\n")
            f.write(f"* TEST {test_id}: {stat_str}, {toggle} changes (Window: {fmt_num(T_S)}p to {fmt_num(T_E)}p)\n")
            f.write("* -------------------------------------------------------------------\n")

            m1_from = T_S + meas1_from
            m1_to = T_S + meas1_to
            m2_from = T_S + meas2_from
            m2_to = T_S + meas2_to

            for out_node in outputs:
                meas_prefix = f"t_{out_node}_{short_toggle}_{short_statics}"

                # Window 1: Input signal goes LOW to HIGH (RISE)
                # Test output for both LH (RISE) and HL (FALL)
                f.write(f".MEASURE TRAN {meas_prefix}_w1_LH TRIG V({toggle}) VAL='0.5 * Vdd_val' RISE=1 TARG V({out_node}) VAL='0.5 * Vdd_val' RISE=1 FROM={fmt_num(m1_from)}p TO={fmt_num(m1_to)}p\n")
                f.write(f".MEASURE TRAN {meas_prefix}_w1_HL TRIG V({toggle}) VAL='0.5 * Vdd_val' RISE=1 TARG V({out_node}) VAL='0.5 * Vdd_val' FALL=1 FROM={fmt_num(m1_from)}p TO={fmt_num(m1_to)}p\n")
                
                # Window 2: Input signal goes HIGH to LOW (FALL)
                # Test output for both LH (RISE) and HL (FALL)
                f.write(f".MEASURE TRAN {meas_prefix}_w2_LH TRIG V({toggle}) VAL='0.5 * Vdd_val' FALL=1 TARG V({out_node}) VAL='0.5 * Vdd_val' RISE=1 FROM={fmt_num(m2_from)}p TO={fmt_num(m2_to)}p\n")
                f.write(f".MEASURE TRAN {meas_prefix}_w2_HL TRIG V({toggle}) VAL='0.5 * Vdd_val' FALL=1 TARG V({out_node}) VAL='0.5 * Vdd_val' FALL=1 FROM={fmt_num(m2_from)}p TO={fmt_num(m2_to)}p\n")
                
                # Append to respective lists
                all_LH_meas[out_node].extend([f"{meas_prefix}_w1_LH", f"{meas_prefix}_w2_LH"])
                all_HL_meas[out_node].extend([f"{meas_prefix}_w1_HL", f"{meas_prefix}_w2_HL"])
            
            f.write("\n")

        f.write("* ===================================================================\n")
        f.write("* Final Delay Calculations (Separated tpLH, tpHL, and Averaged tp)\n")
        f.write("* ===================================================================\n")
        
        final_tps = []
        
        # Calculate MAX LH, MAX HL, and AVG for each output independently
        for out_node in outputs:
            f.write(f"* --- Delays for Output: {out_node} ---\n")
            
            tpLH_name = f"tpLH_{out_node}"
            tpHL_name = f"tpHL_{out_node}"
            
            # MAX of all LH transitions
            f.write(f"* Maximum Low-to-High (tpLH) for {out_node}\n")
            write_cascaded_max(f, all_LH_meas[out_node], tpLH_name)
            
            # MAX of all HL transitions
            f.write(f"* Maximum High-to-Low (tpHL) for {out_node}\n")
            write_cascaded_max(f, all_HL_meas[out_node], tpHL_name)
            
            # Average of tpLH and tpHL
            tp_name = f"tp_{out_node}"
            f.write(f"* Average tp for {out_node}\n")
            f.write(f".MEASURE TRAN {tp_name} PARAM='({tpLH_name} + {tpHL_name}) / 2'\n")
            
            final_tps.append(tp_name)
            f.write("\n")
        
        # Calculate Global MAX (Worst case delay of all averaged tps)
        if len(final_tps) > 1:
            f.write("* --- GLOBAL Worst Case Delay ---\n")
            write_cascaded_max(f, final_tps, "tp_global_max")
        elif len(final_tps) == 1:
            f.write("* --- GLOBAL Worst Case Delay ---\n")
            f.write(f".MEASURE TRAN tp_global_max PARAM='{final_tps[0]}'\n")

    print(f"\nSuccess! The fixed SPICE deck has been written to '{filename}'.")

if __name__ == "__main__":
    generate_spice_deck()
