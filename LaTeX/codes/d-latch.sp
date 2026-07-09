
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

.ENDS D_LATCH
