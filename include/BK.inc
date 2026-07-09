***************** HSPICE Brant-Kung Carry Chain MODELING ***************
*
*   Mohammad Khoshroo - 810102441 
*   Spring 2026
*   AVLSI Course - by Dr. Vahdat
*   Standard MOSFET Model Name : nch , pch
*
.INC "PG.inc"
*
************************* 1-bit BK CARRY CHAIN *************************

.SUBCKT BK1 G1 P1 G0 C0 C1 Vdd Vss scale=1

V_C0 C0 G0 0                                          $ C0

Xlevel1_bit1 G1 P1 G0 C1 Vdd Vss GEN_BLOCK scale=scale  $ C1

.ENDS BK1

************************* 2-bit BK CARRY CHAIN *************************

.SUBCKT BK2 
+ G2 P2 
+ G1 P1 
+ G0 
+ C0 C1 C2 Vdd Vss scale=1

V_C0 C0 G0  0                                         $ C0

Xlevel1_bit1 G1 P1 G0  G10 Vdd Vss GEN_BLOCK scale=scale
V_C1 C1 G10 0                                         $ C1

Xlevel2_bit2 G2 P2 G10 G20 Vdd Vss GEN_BLOCK scale=scale 
V_C2 C2 G20 0                                         $ C2

.ENDS BK2

************************* 4-bit BK CARRY CHAIN *************************

.SUBCKT BK4 
+ G4 P4 
+ G3 P3 
+ G2 P2
+ G1 P1 
+ G0 
+ C0 C1 C2 C3 C4 Vdd Vss scale=1


V_C0 C0 G0  0                                         $ C0

Xlevel1_bit1 G1 P1 G0  G10          Vdd Vss GEN_BLOCK    scale=scale
V_C1 C1 G10 0                                         $ C1

Xlevel1_bit3 G3  P3  G2  P2 G32 P32 Vdd Vss GENPRO_BLOCK scale=scale

Xlevel2_bit3 G32 P32 G10 G30        Vdd Vss GEN_BLOCK    scale=scale
V_C3 C3 G30 0                                         $ C3

Xlevel3_bit2 G2  P2  G10 G20        Vdd Vss GEN_BLOCK    scale=scale 
V_C2 C2 G20 0                                         $ C2

Xlevel3_bit4 G4 P4   G30  G40       Vdd Vss GEN_BLOCK    scale=scale
V_C4 C4 G40 0                                         $ C4

.ENDS BK4

************************* 8-bit BK CARRY CHAIN *************************

.SUBCKT BK8 
+ G8 P8 
+ G7 P7 
+ G6 P6 
+ G5 P5 
+ G4 P4 
+ G3 P3 
+ G2 P2 
+ G1 P1 
+ G0 
+ C0 C1 C2 C3 C4 C5 C6 C7 C8 Vdd Vss scale=1

V_C0 C0 G0  0                                         $ C0

Xlevel1_bit1 G1 P1 G0  G10          Vdd Vss GEN_BLOCK    scale=scale
V_C1 C1 G10 0                                         $ C1

Xlevel1_bit3 G3 P3 G2  P2 G32 P32   Vdd Vss GENPRO_BLOCK scale=scale
Xlevel1_bit5 G5 P5 G4  P4 G54 P54   Vdd Vss GENPRO_BLOCK scale=scale
Xlevel1_bit7 G7 P7 G6  P6 G76 P76   Vdd Vss GENPRO_BLOCK scale=scale

Xlevel2_bit3 G32 P32 G10 G30        Vdd Vss GEN_BLOCK    scale=scale
V_C3 C3 G30 0                                         $ C3

Xlevel2_bit7 G76 P76 G54 P54 G74 P74 Vdd Vss GENPRO_BLOCK scale=scale

Xlevel3_bit7 G74 P74 G30 G70        Vdd Vss GEN_BLOCK    scale=scale
V_C7 C7 G70 0                                         $ C7

Xlevel4_bit5 G54 P54 G30 G50        Vdd Vss GEN_BLOCK    scale=scale
V_C5 C5 G50 0                                         $ C5

Xlevel5_bit2 G2 P2 G10 G20          Vdd Vss GEN_BLOCK    scale=scale
V_C2 C2 G20 0                                         $ C2

Xlevel5_bit4 G4 P4 G30 G40          Vdd Vss GEN_BLOCK    scale=scale
V_C4 C4 G40 0                                         $ C4

Xlevel5_bit6 G6 P6 G50 G60          Vdd Vss GEN_BLOCK    scale=scale
V_C6 C6 G60 0                                         $ C6

Xlevel5_bit8 G8 P8 G70 G80          Vdd Vss GEN_BLOCK    scale=scale
V_C8 C8 G80 0                                         $ C8

.ENDS BK8

