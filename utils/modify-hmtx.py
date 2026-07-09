import os
import io
import math
import pandas as pd
import matplotlib.pyplot as plt

# =====================================================================
# 1. INPUT CONFIGURATIONS
# =====================================================================
FILE_PATH = r"./simulation/BKA/mont-carlo/sim.hmt0.csv" 

# Selected measures to plot (without '_count' suffix)
# Examples: 'i_avg', 'i_peak', 'p_avg', 'p_max', 'pdp', 'tp_avg', 'tp_max', 'vdd_actual'
# Note: Leave empty [] to plot all detected parameters in one figure.
SELECTED_MEASURES = ['tp_avg', 'tp_max', 'vdd_actual','p_avg', 'p_max', "tp_cout" ,"tp_s8"] 

# Output directory and filename
OUTPUT_DIR = "hspice_plots"
OUTPUT_FILENAME = "combined_histograms.png"
os.makedirs(OUTPUT_DIR, exist_ok=True)
# =====================================================================

def load_hspice_csv(file_path):
    """Parses HSPICE output file and removes non-CSV header lines."""
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    header_line_idx = -1
    for idx, line in enumerate(lines):
        clean_line = line.strip().lower()
        
        if clean_line.startswith(("#", "*", "=")):
            continue
            
        if "count" in clean_line and "," in clean_line:
            header_line_idx = idx
            break
            
    if header_line_idx == -1:
        for idx, line in enumerate(lines):
            clean_line = line.strip()
            if not clean_line.startswith(("#", "*", "=")) and "," in clean_line:
                header_line_idx = idx
                break
    
    if header_line_idx == -1:
        raise ValueError("Header columns not found in the file. Please check the CSV structure.")
    
    data_str = "".join(lines[header_line_idx:])
    df = pd.read_csv(io.StringIO(data_str))
    df.columns = df.columns.str.strip()
    return df


try:
    # Read the data
    df = load_hspice_csv(FILE_PATH)
    print("✓ File loaded successfully.")
    
    # Identify parameter value and count columns
    columns = df.columns
    measures = []
    for col in columns:
        if not col.endswith('_count'):
            count_col = f"{col}_count"
            if count_col in columns:
                if len(SELECTED_MEASURES) == 0 or col in SELECTED_MEASURES:
                    measures.append((col, count_col))
                
    if not measures:
        print("⚠ No matching parameters found! Please check SELECTED_MEASURES naming.")
    else:
        num_plots = len(measures)
        print(f"✓ {num_plots} parameters selected for plotting.")

        # Calculate optimal grid size (Rows x Cols) for subplots
        cols = 2 if num_plots > 1 else 1
        rows = math.ceil(num_plots / cols)
        
        # Create a single figure for all plots
        fig, axes = plt.subplots(rows, cols, figsize=(6 * cols, 4.5 * rows))
        
        # Flatten axes array for easy iteration if it's 2D or handle 1D case
        if num_plots == 1:
            axes = [axes]
        else:
            axes = axes.flatten()
            
        # Define a list of distinct colors for subplots
        color_palette = [
            '#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', 
            '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', 
            '#bcbd22', '#17becf', '#4e79a7', '#f28e2b'
        ]
            
        # Plot each parameter in its respective subplot
        for i, (val_col, count_col) in enumerate(measures):
            ax = axes[i]
            bin_centers = df[val_col].values
            counts = df[count_col].values
            
            # Calculate dynamic bar width
            if len(bin_centers) > 1:
                width = (bin_centers[1] - bin_centers[0]) * 0.8
            else:
                width = 0.1
                
            # Assign a unique color based on the index
            plot_color = color_palette[i % len(color_palette)]
                
            ax.bar(bin_centers, counts, width=width, color=plot_color, edgecolor='black', alpha=0.8)
            
            # Subplot styling
            ax.set_title(f'Histogram for {val_col.upper()}', fontsize=11, fontweight='bold', color='#333333')
            ax.set_xlabel('Value', fontsize=9)
            ax.set_ylabel('Count (Frequency)', fontsize=9)
            ax.grid(axis='y', linestyle='--', alpha=0.5)
            ax.tick_params(axis='both', labelsize=8)
            
        # Hide any unused subplots (if grid size is larger than actual plots)
        for j in range(num_plots, len(axes)):
            fig.delaxes(axes[j])
            
        # Save the combined figure
        save_path = os.path.join(OUTPUT_DIR, OUTPUT_FILENAME)
        plt.tight_layout()
        plt.savefig(save_path, dpi=150)
        plt.close()
        
        print(f"✓ Combined plot successfully saved to '{save_path}'")

except Exception as e:
    print(f"Error during execution: {e}")
