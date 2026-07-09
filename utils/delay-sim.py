def generate_spice_deck():

    signals = ["A", "B", "Cin"]
    outputs = ["S", "Cout"]

    W = 500.0
    delta_t = 50.0
    t_start = 75.0

    temp = 25

    vdd_var = "Vdd_val"
    data_name = "FA_TRANSISSION"

    filename = "delay.sp"
    
#########################################################################

    data_rows = []
    test_id = 1

    # ==================================================
    # Generate Test Vectors
    # ==================================================

    for toggle_idx, toggle_sig in enumerate(signals):

        other_sigs = (
            signals[:toggle_idx]
            + signals[toggle_idx + 1:]
        )

        for b in range(2 ** (len(signals) - 1)):

            static_states = {}

            for bit_idx, other_sig in enumerate(other_sigs):

                static_states[other_sig] = (
                    (b >> bit_idx) & 1
                )

            row_rise = {toggle_sig: (0, 1)}
            row_fall = {toggle_sig: (1, 0)}

            for sig, state in static_states.items():

                row_rise[sig] = (state, state)
                row_fall[sig] = (state, state)

            rise_vals = []
            fall_vals = []

            for sig in signals:

                rise_vals.extend(row_rise[sig])
                fall_vals.extend(row_fall[sig])

            data_rows.append(
                (
                    *rise_vals,
                    0,                      # is_fall_transition
                    f"SWITCH={toggle_sig}"
                )
            )

            data_rows.append(
                (
                    *fall_vals,
                    1,                      # is_fall_transition
                    f"SWITCH={toggle_sig}"
                )
            )

            test_id += 1

    # ==================================================
    # Write SPICE File
    # ==================================================

    with open(filename, "w") as f:

        f.write(
            f".TRAN 0.01p {W}p "
            f"SWEEP DATA={data_name}\n"
        )

        f.write(f".TEMP {temp}\n\n")

        # ----------------------------------------------
        # Input Stimulus
        # ----------------------------------------------

        for sig in signals:

            s = sig.lower()

            f.write(
                f"V{sig} {sig} 0 "
                f"PWL("
                f"0p '{s}_init*{vdd_var}' "
                f"{t_start}p '{s}_init*{vdd_var}' "
                f"{t_start + delta_t}p '{s}_final*{vdd_var}' "
                f"{W}p '{s}_final*{vdd_var}'"
                f")\n"
            )

        f.write("\n")

        # ----------------------------------------------
        # DATA TABLE
        # ----------------------------------------------

        f.write(f".DATA {data_name}\n")

        header = []

        for sig in signals:

            header.extend([
                f"{sig.lower()}_init",
                f"{sig.lower()}_final"
            ])

        header.append("is_fall_transition")

        f.write("+ " + " ".join(header) + "\n")

        for row in data_rows:

            numeric_values = row[:-1]
            switch_comment = row[-1]

            f.write(
                "+ "
                + " ".join(
                    f"{str(v):<8}"
                    for v in numeric_values
                )
                + f" $ {switch_comment}\n"
            )

        f.write(".ENDDATA\n\n")

        # ----------------------------------------------
        # Delay Measurements
        # ----------------------------------------------

        td = t_start - 10

        for inp in signals:

            for out in outputs:

                f.write(
                    f".MEASURE TRAN "
                    f"tpLH_{out}_{inp} "
                    f"TRIG V({inp}) "
                    f"VAL='0.5*{vdd_var}' "
                    f"RISE=1 "
                    f"TD={td}p "
                    f"TARG V({out}) "
                    f"VAL='0.5*{vdd_var}' "
                    f"RISE=1\n"
                )

                f.write(
                    f".MEASURE TRAN "
                    f"tpHL_{out}_{inp} "
                    f"TRIG V({inp}) "
                    f"VAL='0.5*{vdd_var}' "
                    f"FALL=1 "
                    f"TD={td}p "
                    f"TARG V({out}) "
                    f"VAL='0.5*{vdd_var}' "
                    f"FALL=1\n"
                )

        f.write("\n")
        
    print(
        f"✔ SPICE deck written to '{filename}'"
    )


if __name__ == "__main__":
    generate_spice_deck()