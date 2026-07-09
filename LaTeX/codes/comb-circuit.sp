
************************** COMB-CISRCUIT .SUBCKT *********************

.subckt CIRCUIT A B C D OUT Vdd Vss

Xnand1  A        B          nand_ab         Vdd Vss  NAND2       scale=2.2
Xnor1   B        C          nor_bc          Vdd Vss  NOR2        scale=2.8
Xinv1   D        inv_d                      Vdd Vss  INV         scale=1.2

Xxor1   nand_ab  nor_bc     xor_out         Vdd Vss  XOR2_SYM    scale=3.4
Xxnor1  nor_bc   inv_d      xnor_out        Vdd Vss  XNOR2_SYM   scale=3.8

Xnand2  xor_out  xnor_out   nand2_out       Vdd Vss  NAND2       scale=2.4

Xnor3   xor_out  nand2_out  xnor_out  OUT   Vdd Vss  NOR3        scale=5

$ Load Capacitor
CLoad   OUT  Vss  100f  

.ends CIRCUIT