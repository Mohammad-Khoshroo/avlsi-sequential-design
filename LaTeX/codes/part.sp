
************************** LATCH-PIPE 2level .SUBCKT *********************

.subckt LATCH_PIPE_P1 A B C D CLK OUT_l Vdd Vss

Xinv_clk  CLK  CLK_bar  Vdd Vss  INV  scale=1

$ LATCH
Xlatch_A  A  CLK  A_l  A_l_bar  Vdd Vss  D_LATCH_NN  scale=1
Xlatch_B  B  CLK  B_l  B_l_bar  Vdd Vss  D_LATCH_NN  scale=1
Xlatch_C  C  CLK  C_l  C_l_bar  Vdd Vss  D_LATCH_NN  scale=1
Xlatch_D  D  CLK  D_l  D_l_bar  Vdd Vss  D_LATCH_NN  scale=1

Xnand1  A_l  B_l  nand_ab   Vdd Vss  NAND2      scale=2.2
Xnor1   B_l  C_l  nor_bc    Vdd Vss  NOR2       scale=2.8
Xinv1   D_l             inv_d     Vdd Vss  INV        scale=1.2

Xxor1   nand_ab    nor_bc     xor_out   Vdd Vss  XOR2_SYM   scale=3.4
Xxnor1  nor_bc     inv_d      xnor_out  Vdd Vss  XNOR2_SYM  scale=3.8

$ LATCH
Xlatch_xor   xor_out   CLK_bar  xor_l   xor_l_bar   Vdd Vss  D_LATCH_NN  scale=1
Xlatch_xnor  xnor_out  CLK_bar  xnor_l  xnor_l_bar  Vdd Vss  D_LATCH_NN  scale=1

Xnand2  xor_l  xnor_l  and_out       Vdd Vss  AND2  scale=2.4
Xnor3   xor_l  and_out       xnor_l  OUT  Vdd Vss  NOR3  scale=5

CLoad   OUT  Vss  100f  

$ LATCH
Xlatch_out  OUT  CLK  OUT_l  OUT_l_bar  Vdd Vss  D_LATCH_NN  scale=1

.ends LATCH_PIPE_P1


.subckt LATCH_PIPE_P2 A B C D CLK OUT_l Vdd Vss

Xinv_clk  CLK  CLK_bar  Vdd Vss  INV  scale=1

$ LATCH
Xlatch_A  A  CLK  A_l  A_l_bar  Vdd Vss  D_LATCH_NN  scale=1
Xlatch_B  B  CLK  B_l  B_l_bar  Vdd Vss  D_LATCH_NN  scale=1
Xlatch_C  C  CLK  C_l  C_l_bar  Vdd Vss  D_LATCH_NN  scale=1
Xlatch_D  D  CLK  D_l  D_l_bar  Vdd Vss  D_LATCH_NN  scale=1

Xnand1  A_l  B_l  nand_ab   Vdd Vss  NAND2      scale=2.2
Xnor1   B_l  C_l  nor_bc    Vdd Vss  NOR2       scale=2.8
Xinv1   D_l             inv_d     Vdd Vss  INV        scale=1.2

$ LATCH
Xlatch_nand  nand_ab  CLK_bar  nand_ab_l  nand_ab_l_bar  Vdd Vss  D_LATCH_NN  scale=1
Xlatch_nor   nor_bc   CLK_bar  nor_bc_l   nor_bc_l_bar   Vdd Vss  D_LATCH_NN  scale=1
Xlatch_inv   inv_d    CLK_bar  inv_d_l    inv_d_l_bar    Vdd Vss  D_LATCH_NN  scale=1

Xxor1   nand_ab_l  nor_bc_l   xor_out   Vdd Vss  XOR2_SYM   scale=3.4
Xxnor1  nor_bc_l   inv_d_l    xnor_out  Vdd Vss  XNOR2_SYM  scale=3.8

Xnand2  xor_out      xnor_out     and_out   Vdd Vss  AND2       scale=2.4
Xnor3   xor_out      and_out      xnor_out  OUT  Vdd Vss    NOR3       scale=5

CLoad   OUT  Vss  100f  

$ LATCH
Xlatch_out  OUT  CLK  OUT_l  OUT_l_bar  Vdd Vss  D_LATCH_NN  scale=1

.ends LATCH_PIPE_P2
