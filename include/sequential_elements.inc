******************** HSPICE BASIC GATES MODELING ********************
*
*   Mohammad Khoshroo - 810102441 
*   Spring 2026
*   AVLSI Course - by Dr. Vahdat
*   Standard MOSFET Model Name : nmos , pmos
*

.INC "basic_gates.inc"

************************** D LATCH .SUBCKT **************************

$ E is the Enable signal 
$ E == CLK  => Positive-Level Sensitive
$ E == ~CLK => Negative-Level Sensitive

.SUBCKT D_LATCH_NN D E Q Q_bar Vdd Vss scale=1

Xinv_D  D       D_not            Vdd Vss  INV    scale=scale

Xnand1  D       E       N1       Vdd Vss  NAND2  scale=scale
Xnand2  D_not   E       N2       Vdd Vss  NAND2  scale=scale

$ Cross-coupled NAND
Xnand3  N1      Q_bar   Q        Vdd Vss  NAND2  scale=scale
Xnand4  N2      Q       Q_bar    Vdd Vss  NAND2  scale=scale

.ENDS D_LATCH_NN

.SUBCKT NEG_D_LATCH_NN D E Q Q_bar Vdd Vss scale=1

Xinv_D  D       D_not            Vdd Vss  INV    scale=scale
Xinv_D  E       E_not            Vdd Vss  INV    scale=scale

Xnand1  D       E_not       N1       Vdd Vss  NAND2  scale=scale
Xnand2  D_not   E_not       N2       Vdd Vss  NAND2  scale=scale

$ Cross-coupled NAND
Xnand3  N1      Q_bar   Q        Vdd Vss  NAND2  scale=scale
Xnand4  N2      Q       Q_bar    Vdd Vss  NAND2  scale=scale

.ENDS NEG_D_LATCH_NN


****************** D FLIP-FLOP - REGISTER .SUBCKT *******************

$ PosEdge Master-Slave D Flip-Flop

.SUBCKT D_FF_POS D Clk Q Q_bar Vdd Vss scale=1

Xinv_clk1  Clk        Clk_bar  Vdd Vss  INV  scale=scale
Xinv_clk2  Clk_bar    Clk_buf  Vdd Vss  INV  scale=scale


$ Master D-Latch (Neg)
Xmaster    D          Clk_bar  Qm       Qm_bar   Vdd Vss  D_LATCH  scale=scale

$ Slave  D-Latch (pos)
Xslave     Qm         Clk_buf  Q        Q_bar    Vdd Vss  D_LATCH  scale=scale

.ENDS D_FF_POS

**************** D FLIP-FLOP - Neg REGISTER .SUBCKT *****************

$ NegEdge-Triggered Master-Slave D Flip-Flop

.SUBCKT D_FF_NEG D Clk Q Q_bar Vdd Vss scale=1

Xinv_clk1  Clk        Clk_bar  Vdd Vss  INV  scale=scale
Xinv_clk2  Clk_bar    Clk_buf  Vdd Vss  INV  scale=scale

* Master D-Latch (pos)
Xmaster    D          Clk_buf  Qm       Qm_bar   Vdd Vss  D_LATCH  scale=scale

* Slave  D-Latch (neg) 
Xslave     Qm         Clk_bar  Q        Q_bar    Vdd Vss  D_LATCH  scale=scale

.ENDS D_FF_NEG
