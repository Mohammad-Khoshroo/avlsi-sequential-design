
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
