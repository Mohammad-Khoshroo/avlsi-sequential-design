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

************************** LATCH-PIPE .SUBCKT **************************

.SUBCKT LATCH_PIPE A B C D Clk OUT Vdd Vss scale=1

Xlatch_a   A   Clk   A_l   A_l_bar   Vdd Vss  D_LATCH_NN  scale=scale
Xlatch_b   B   Clk   B_l   B_l_bar   Vdd Vss  D_LATCH_NN  scale=scale
Xlatch_c   C   Clk   C_l   C_l_bar   Vdd Vss  D_LATCH_NN  scale=scale
Xlatch_d   D   Clk   D_l   D_l_bar   Vdd Vss  D_LATCH_NN  scale=scale

Xlogic A_l    B_l   C_l   D_l   comb_out     Vdd Vss  CIRCUIT

$ It's what i say on part one of report
Xinv_CLK  CLK       CLK_not            Vdd Vss  INV    scale=scale

Xlatch_out comb_out Clk_not OUT   OUT_bar Vdd Vss  D_LATCH_NN  scale=scale

.ENDS LATCH_PIPE
