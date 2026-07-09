import io
import matplotlib.pyplot as plt
import pandas as pd

FILE_PATH = r"./simulation/BKA/mont-carlo/sim.qqt0.csv"

PARAMETERS_TO_PLOT = ["tp_avg", "p_avg", "vdd_actual",]

X_AXIS_PARAMETER = "StdNormalQuantiles"

SAVE_PLOT_PATH = "hspice_plot.png"
# ==================================================================


def load_hspice_csv(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    start_idx = -1
    for i, line in enumerate(lines):
        clean_line = line.strip()
        if "i_avg" in clean_line and "StdNormalQuantiles" in clean_line:
            start_idx = i
            break
            
    if start_idx == -1:
        max_commas = 0
        for i, line in enumerate(lines):
            clean_line = line.strip()
            if clean_line.startswith(("#", "*", "=")):
                continue
            
            comma_count = clean_line.count(",")
            if comma_count > max_commas and comma_count >= 3: 
                max_commas = comma_count
                start_idx = i

    if start_idx == -1:
        raise ValueError("Header with valid columns not found.")

    csv_data = "".join(lines[start_idx:])
    
    return pd.read_csv(io.StringIO(csv_data), on_bad_lines='skip')

def main():
    try:
        df = load_hspice_csv(FILE_PATH)
        print("fields founded:")
        print(list(df.columns))

        fig, ax1 = plt.subplots(figsize=(10, 6))

        use_x = X_AXIS_PARAMETER and X_AXIS_PARAMETER in df.columns
        if use_x:
            df = df.sort_values(by=X_AXIS_PARAMETER)
            x_data = df[X_AXIS_PARAMETER]
            ax1.set_xlabel(X_AXIS_PARAMETER, fontsize=11, fontweight="bold")
        else:
            x_data = df.index
            ax1.set_xlabel("Sample Index", fontsize=11, fontweight="bold")

        cmap = plt.get_cmap("tab10")
        
        for i, param in enumerate(PARAMETERS_TO_PLOT):
            df.columns = df.columns.str.strip()
            param = param.strip()

            if param not in df.columns:
                print(f"parameter {param} not found")
                continue

            if i == 0:
                ax = ax1
                ax.set_ylabel(param, color = cmap(i % 10), fontsize=11)
            else:
                ax = ax1.twinx()
                ax.spines["right"].set_position(("outward", 70 * (i - 1)))
                ax.set_ylabel(param, color = cmap(i % 10), fontsize=10)

            ax.plot(
                x_data,
                df[param],
                marker="o",
                linestyle="-",
                color = cmap(i % 10),
                label=param,
                alpha=0.8,
            )
            ax.tick_params(axis="y", labelcolor=cmap(i % 10))
            ax.grid(True, linestyle=":", alpha=0.6)

        plt.title("Q-Q (Quantile-Quantile) Plot", fontsize=14, fontweight="bold")
        fig.tight_layout()

        plt.savefig(SAVE_PLOT_PATH, dpi=300)
        print(f"Done")
        
        plt.show()
        
    except FileNotFoundError:
        print(f"file not found")

if __name__ == "__main__":
    main()
