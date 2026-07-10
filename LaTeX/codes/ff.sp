
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