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

************************** LATCH-PIPE 2level .SUBCKT *********************

.subckt LATCH_PIPE_P1 A B C D CLK OUT_l Vdd Vss

Xinv_clk  CLK  CLK_bar  Vdd Vss  INV  scale=1

Xlatch_A  A  CLK  A_l  A_l_bar  Vdd Vss  D_LATCH_NN  scale=1
Xlatch_B  B  CLK  B_l  B_l_bar  Vdd Vss  D_LATCH_NN  scale=1
Xlatch_C  C  CLK  C_l  C_l_bar  Vdd Vss  D_LATCH_NN  scale=1
Xlatch_D  D  CLK  D_l  D_l_bar  Vdd Vss  D_LATCH_NN  scale=1

Xnand1  A_l  B_l  nand_ab   Vdd Vss  NAND2      scale=2.2
Xnor1   B_l  C_l  nor_bc    Vdd Vss  NOR2       scale=2.8
Xinv1   D_l             inv_d     Vdd Vss  INV        scale=1.2

Xxor1   nand_ab    nor_bc     xor_out   Vdd Vss  XOR2_SYM   scale=3.4
Xxnor1  nor_bc     inv_d      xnor_out  Vdd Vss  XNOR2_SYM  scale=3.8

Xlatch_xor   xor_out   CLK_bar  xor_l   xor_l_bar   Vdd Vss  D_LATCH_NN  scale=1
Xlatch_xnor  xnor_out  CLK_bar  xnor_l  xnor_l_bar  Vdd Vss  D_LATCH_NN  scale=1

Xnand2  xor_l  xnor_l  and_out       Vdd Vss  AND2  scale=2.4
Xnor3   xor_l  and_out       xnor_l  OUT  Vdd Vss  NOR3  scale=5

CLoad   OUT  Vss  100f  


Xlatch_out  OUT  CLK  OUT_l  OUT_l_bar  Vdd Vss  D_LATCH_NN  scale=1

.ends LATCH_PIPE_P1


.subckt LATCH_PIPE_P2 A B C D CLK OUT_l Vdd Vss

Xinv_clk  CLK  CLK_bar  Vdd Vss  INV  scale=1

Xlatch_A  A  CLK  A_l  A_l_bar  Vdd Vss  D_LATCH_NN  scale=1
Xlatch_B  B  CLK  B_l  B_l_bar  Vdd Vss  D_LATCH_NN  scale=1
Xlatch_C  C  CLK  C_l  C_l_bar  Vdd Vss  D_LATCH_NN  scale=1
Xlatch_D  D  CLK  D_l  D_l_bar  Vdd Vss  D_LATCH_NN  scale=1

Xnand1  A_l  B_l  nand_ab   Vdd Vss  NAND2      scale=2.2
Xnor1   B_l  C_l  nor_bc    Vdd Vss  NOR2       scale=2.8
Xinv1   D_l             inv_d     Vdd Vss  INV        scale=1.2

Xlatch_nand  nand_ab  CLK_bar  nand_ab_l  nand_ab_l_bar  Vdd Vss  D_LATCH_NN  scale=1
Xlatch_nor   nor_bc   CLK_bar  nor_bc_l   nor_bc_l_bar   Vdd Vss  D_LATCH_NN  scale=1
Xlatch_inv   inv_d    CLK_bar  inv_d_l    inv_d_l_bar    Vdd Vss  D_LATCH_NN  scale=1

Xxor1   nand_ab_l  nor_bc_l   xor_out   Vdd Vss  XOR2_SYM   scale=3.4
Xxnor1  nor_bc_l   inv_d_l    xnor_out  Vdd Vss  XNOR2_SYM  scale=3.8

Xnand2  xor_out      xnor_out     and_out   Vdd Vss  AND2       scale=2.4
Xnor3   xor_out      and_out      xnor_out  OUT  Vdd Vss    NOR3       scale=5

CLoad   OUT  Vss  100f  

Xlatch_out  OUT  CLK  OUT_l  OUT_l_bar  Vdd Vss  D_LATCH_NN  scale=1

.ends LATCH_PIPE_P2
