******************** HSPICE BASIC GATES MODELING ********************
*
*   Mohammad Khoshroo - 810102441 
*   Spring 2026
*   AVLSI Course - by Dr. Vahdat
*   Standard MOSFET Model Name : nmos , pmos
*

.INC "sequential_elements.inc"
.INC "comb_circuit.inc"

************************** REG-PIPE .SUBCKT **************************

.SUBCKT REG_PIPE A B C D Clk OUT Vdd Vss scale=1

Xffa   A   Clk   A_r   A_r_bar   Vdd Vss  D_FF_POS  scale=scale
Xffb   B   Clk   B_r   B_r_bar   Vdd Vss  D_FF_POS  scale=scale
Xffc   C   Clk   C_r   C_r_bar   Vdd Vss  D_FF_POS  scale=scale
Xffd   D   Clk   D_r   D_r_bar   Vdd Vss  D_FF_POS  scale=scale

Xlogic A_r    B_r   C_r   D_r   comb_out     Vdd Vss  CIRCUIT

Xffout comb_out Clk OUT   OUT_bar Vdd Vss  D_FF_POS  scale=scale

.ENDS REG_PIPE
