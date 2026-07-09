***************** HSPICE BITWISE PG LOGIC MODELING ******************
*
*   Mohammad Khoshroo - 810102441 
*   Spring 2026
*   AVLSI Course - by Dr. Vahdat
*   Standard MOSFET Model Name : nch , pch
*
*
.INC "basic_gates.inc"
*
****************************** GEN .SUBCKT *****************************

.SUBCKT GEN_BLOCK G_ik P_ik G_kj G_ij Vdd Vss scale=1 $ Gray Block (generates G_ij)

$ P_ik & G_kj
Xand  P_ik  G_kj  mid   Vdd  Vss  AND2  scale=scale

$ G_ij = G_ik | (P_ik & G_kj)
Xor   G_ik  mid      G_ij  Vdd  Vss  OR2   scale=scale

.ENDS GEN_BLOCK

**************************** GENPRO .SUBCKT ****************************

.SUBCKT GENPRO_BLOCK G_ik P_ik G_kj P_kj G_ij P_ij Vdd Vss scale=1 $ Black Block (generates both G_ij and P_ij)

$ G_ij = G_ik | (P_ik & G_kj)
Xgen G_ik P_ik G_kj G_ij Vdd Vss GEN_BLOCK scale=scale 

$ P_ij = P_ik & P_kj
Xand  P_ik  P_kj  P_ij  Vdd  Vss  AND2  scale=scale

.ENDS GENPRO_BLOCK

********************* BASE BITWISE PG .SUBCKT *********************

.SUBCKT PG A B G P Vdd Vss scale=1

Xand1 A B G Vdd Vss AND2 scale=scale
Xxor1 A B P Vdd Vss XOR2 scale=scale

.ENDS PG

********************* 1-bit BITWISE PG .SUBCKT *********************

.SUBCKT PG1 A1 B1 Cin G1 P1 G0 P0 Vdd Vss scale=1

Xbit1  A1 B1 G1 P1 Vdd Vss PG scale=scale

V_G0   G0 Cin 0
V_P0   P0 Vss 0

.ENDS PG1

********************* 2-bit BITWISE PG .SUBCKT *********************

.SUBCKT PG2 A1 A2 B1 B2 Cin G1 G2 P1 P2 G0 P0 Vdd Vss scale=1

Xbit1  A1 B1 G1 P1 Vdd Vss PG scale=scale
Xbit2  A2 B2 G2 P2 Vdd Vss PG scale=scale

V_G0   G0 Cin 0
V_P0   P0 Vss 0

.ENDS PG2

********************* 4-bit BITWISE PG .SUBCKT *********************

.SUBCKT PG4 A1 A2 A3 A4 B1 B2 B3 B4 Cin G1 G2 G3 G4 P1 P2 P3 P4 G0 P0 Vdd Vss scale=1

Xbit1  A1 B1 G1 P1 Vdd Vss PG scale=scale
Xbit2  A2 B2 G2 P2 Vdd Vss PG scale=scale
Xbit3  A3 B3 G3 P3 Vdd Vss PG scale=scale
Xbit4  A4 B4 G4 P4 Vdd Vss PG scale=scale

V_G0   G0 Cin 0
V_P0   P0 Vss 0

.ENDS PG4

********************* 8-bit BITWISE PG .SUBCKT *********************

.SUBCKT PG8 A1 A2 A3 A4 A5 A6 A7 A8 B1 B2 B3 B4 B5 B6 B7 B8 Cin 
+ G1 G2 G3 G4 G5 G6 G7 G8 P1 P2 P3 P4 P5 P6 P7 P8 G0 P0 Vdd Vss scale=1

Xbit1  A1 B1 G1 P1 Vdd Vss PG scale=scale
Xbit2  A2 B2 G2 P2 Vdd Vss PG scale=scale
Xbit3  A3 B3 G3 P3 Vdd Vss PG scale=scale
Xbit4  A4 B4 G4 P4 Vdd Vss PG scale=scale
Xbit5  A5 B5 G5 P5 Vdd Vss PG scale=scale
Xbit6  A6 B6 G6 P6 Vdd Vss PG scale=scale
Xbit7  A7 B7 G7 P7 Vdd Vss PG scale=scale
Xbit8  A8 B8 G8 P8 Vdd Vss PG scale=scale

V_G0   G0 Cin 0
V_P0   P0 Vss 0

.ENDS PG8

********************* 16-bit BITWISE PG .SUBCKT *********************

.SUBCKT PG16 
+ A1 A2 A3 A4 A5 A6 A7 A8 A9 A10 A11 A12 A13 A14 A15 A16 
+ B1 B2 B3 B4 B5 B6 B7 B8 B9 B10 B11 B12 B13 B14 B15 B16 Cin 
+ G1 G2 G3 G4 G5 G6 G7 G8 G9 G10 G11 G12 G13 G14 G15 G16 
+ P1 P2 P3 P4 P5 P6 P7 P8 P9 P10 P11 P12 P13 P14 P15 P16 
+ G0 P0 Vdd Vss scale=1

Xbit1  A1  B1  G1  P1  Vdd Vss PG scale=scale
Xbit2  A2  B2  G2  P2  Vdd Vss PG scale=scale
Xbit3  A3  B3  G3  P3  Vdd Vss PG scale=scale
Xbit4  A4  B4  G4  P4  Vdd Vss PG scale=scale
Xbit5  A5  B5  G5  P5  Vdd Vss PG scale=scale
Xbit6  A6  B6  G6  P6  Vdd Vss PG scale=scale
Xbit7  A7  B7  G7  P7  Vdd Vss PG scale=scale
Xbit8  A8  B8  G8  P8  Vdd Vss PG scale=scale
Xbit9  A9  B9  G9  P9  Vdd Vss PG scale=scale
Xbit10 A10 B10 G10 P10 Vdd Vss PG scale=scale
Xbit11 A11 B11 G11 P11 Vdd Vss PG scale=scale
Xbit12 A12 B12 G12 P12 Vdd Vss PG scale=scale
Xbit13 A13 B13 G13 P13 Vdd Vss PG scale=scale
Xbit14 A14 B14 G14 P14 Vdd Vss PG scale=scale
Xbit15 A15 B15 G15 P15 Vdd Vss PG scale=scale
Xbit16 A16 B16 G16 P16 Vdd Vss PG scale=scale

V_G0   G0 Cin 0
V_P0   P0 Vss 0

.ENDS PG16

********************* 32-bit BITWISE PG .SUBCKT *********************

.SUBCKT PG32
+ A1 A2 A3 A4 A5 A6 A7 A8 A9 A10 A11 A12 A13 A14 A15 A16
+ A17 A18 A19 A20 A21 A22 A23 A24 A25 A26 A27 A28 A29 A30 A31 A32
+ B1 B2 B3 B4 B5 B6 B7 B8 B9 B10 B11 B12 B13 B14 B15 B16
+ B17 B18 B19 B20 B21 B22 B23 B24 B25 B26 B27 B28 B29 B30 B31 B32 Cin
+ G1 G2 G3 G4 G5 G6 G7 G8 G9 G10 G11 G12 G13 G14 G15 G16
+ G17 G18 G19 G20 G21 G22 G23 G24 G25 G26 G27 G28 G29 G30 G31 G32
+ P1 P2 P3 P4 P5 P6 P7 P8 P9 P10 P11 P12 P13 P14 P15 P16
+ P17 P18 P19 P20 P21 P22 P23 P24 P25 P26 P27 P28 P29 P30 P31 P32
+ G0 P0 Vdd Vss scale=1

Xbit1  A1  B1  G1  P1  Vdd Vss PG scale=scale
Xbit2  A2  B2  G2  P2  Vdd Vss PG scale=scale
Xbit3  A3  B3  G3  P3  Vdd Vss PG scale=scale
Xbit4  A4  B4  G4  P4  Vdd Vss PG scale=scale
Xbit5  A5  B5  G5  P5  Vdd Vss PG scale=scale
Xbit6  A6  B6  G6  P6  Vdd Vss PG scale=scale
Xbit7  A7  B7  G7  P7  Vdd Vss PG scale=scale
Xbit8  A8  B8  G8  P8  Vdd Vss PG scale=scale
Xbit9  A9  B9  G9  P9  Vdd Vss PG scale=scale
Xbit10 A10 B10 G10 P10 Vdd Vss PG scale=scale
Xbit11 A11 B11 G11 P11 Vdd Vss PG scale=scale
Xbit12 A12 B12 G12 P12 Vdd Vss PG scale=scale
Xbit13 A13 B13 G13 P13 Vdd Vss PG scale=scale
Xbit14 A14 B14 G14 P14 Vdd Vss PG scale=scale
Xbit15 A15 B15 G15 P15 Vdd Vss PG scale=scale
Xbit16 A16 B16 G16 P16 Vdd Vss PG scale=scale
Xbit17 A17 B17 G17 P17 Vdd Vss PG scale=scale
Xbit18 A18 B18 G18 P18 Vdd Vss PG scale=scale
Xbit19 A19 B19 G19 P19 Vdd Vss PG scale=scale
Xbit20 A20 B20 G20 P20 Vdd Vss PG scale=scale
Xbit21 A21 B21 G21 P21 Vdd Vss PG scale=scale
Xbit22 A22 B22 G22 P22 Vdd Vss PG scale=scale
Xbit23 A23 B23 G23 P23 Vdd Vss PG scale=scale
Xbit24 A24 B24 G24 P24 Vdd Vss PG scale=scale
Xbit25 A25 B25 G25 P25 Vdd Vss PG scale=scale
Xbit26 A26 B26 G26 P26 Vdd Vss PG scale=scale
Xbit27 A27 B27 G27 P27 Vdd Vss PG scale=scale
Xbit28 A28 B28 G28 P28 Vdd Vss PG scale=scale
Xbit29 A29 B29 G29 P29 Vdd Vss PG scale=scale
Xbit30 A30 B30 G30 P30 Vdd Vss PG scale=scale
Xbit31 A31 B31 G31 P31 Vdd Vss PG scale=scale
Xbit32 A32 B32 G32 P32 Vdd Vss PG scale=scale

V_G0   G0 Cin 0
V_P0   P0 Vss 0

.ENDS PG32

********************* 64-bit BITWISE PG .SUBCKT *********************

.SUBCKT PG64
+ A1 A2 A3 A4 A5 A6 A7 A8 A9 A10 A11 A12 A13 A14 A15 A16
+ A17 A18 A19 A20 A21 A22 A23 A24 A25 A26 A27 A28 A29 A30 A31 A32
+ A33 A34 A35 A36 A37 A38 A39 A40 A41 A42 A43 A44 A45 A46 A47 A48
+ A49 A50 A51 A52 A53 A54 A55 A56 A57 A58 A59 A60 A61 A62 A63 A64
+ B1 B2 B3 B4 B5 B6 B7 B8 B9 B10 B11 B12 B13 B14 B15 B16
+ B17 B18 B19 B20 B21 B22 B23 B24 B25 B26 B27 B28 B29 B30 B31 B32
+ B33 B34 B35 B36 B37 B38 B39 B40 B41 B42 B43 B44 B45 B46 B47 B48
+ B49 B50 B51 B52 B53 B54 B55 B56 B57 B58 B59 B60 B61 B62 B63 B64 Cin
+ G1 G2 G3 G4 G5 G6 G7 G8 G9 G10 G11 G12 G13 G14 G15 G16
+ G17 G18 G19 G20 G21 G22 G23 G24 G25 G26 G27 G28 G29 G30 G31 G32
+ G33 G34 G35 G36 G37 G38 G39 G40 G41 G42 G43 G44 G45 G46 G47 G48
+ G49 G50 G51 G52 G53 G54 G55 G56 G57 G58 G59 G60 G61 G62 G63 G64
+ P1 P2 P3 P4 P5 P6 P7 P8 P9 P10 P11 P12 P13 P14 P15 P16
+ P17 P18 P19 P20 P21 P22 P23 P24 P25 P26 P27 P28 P29 P30 P31 P32
+ P33 P34 P35 P36 P37 P38 P39 P40 P41 P42 P43 P44 P45 P46 P47 P48
+ P49 P50 P51 P52 P53 P54 P55 P56 P57 P58 P59 P60 P61 P62 P63 P64
+ G0 P0 Vdd Vss scale=1

Xbit1  A1  B1  G1  P1  Vdd Vss PG scale=scale
Xbit2  A2  B2  G2  P2  Vdd Vss PG scale=scale
Xbit3  A3  B3  G3  P3  Vdd Vss PG scale=scale
Xbit4  A4  B4  G4  P4  Vdd Vss PG scale=scale
Xbit5  A5  B5  G5  P5  Vdd Vss PG scale=scale
Xbit6  A6  B6  G6  P6  Vdd Vss PG scale=scale
Xbit7  A7  B7  G7  P7  Vdd Vss PG scale=scale
Xbit8  A8  B8  G8  P8  Vdd Vss PG scale=scale
Xbit9  A9  B9  G9  P9  Vdd Vss PG scale=scale
Xbit10 A10 B10 G10 P10 Vdd Vss PG scale=scale
Xbit11 A11 B11 G11 P11 Vdd Vss PG scale=scale
Xbit12 A12 B12 G12 P12 Vdd Vss PG scale=scale
Xbit13 A13 B13 G13 P13 Vdd Vss PG scale=scale
Xbit14 A14 B14 G14 P14 Vdd Vss PG scale=scale
Xbit15 A15 B15 G15 P15 Vdd Vss PG scale=scale
Xbit16 A16 B16 G16 P16 Vdd Vss PG scale=scale
Xbit17 A17 B17 G17 P17 Vdd Vss PG scale=scale
Xbit18 A18 B18 G18 P18 Vdd Vss PG scale=scale
Xbit19 A19 B19 G19 P19 Vdd Vss PG scale=scale
Xbit20 A20 B20 G20 P20 Vdd Vss PG scale=scale
Xbit21 A21 B21 G21 P21 Vdd Vss PG scale=scale
Xbit22 A22 B22 G22 P22 Vdd Vss PG scale=scale
Xbit23 A23 B23 G23 P23 Vdd Vss PG scale=scale
Xbit24 A24 B24 G24 P24 Vdd Vss PG scale=scale
Xbit25 A25 B25 G25 P25 Vdd Vss PG scale=scale
Xbit26 A26 B26 G26 P26 Vdd Vss PG scale=scale
Xbit27 A27 B27 G27 P27 Vdd Vss PG scale=scale
Xbit28 A28 B28 G28 P28 Vdd Vss PG scale=scale
Xbit29 A29 B29 G29 P29 Vdd Vss PG scale=scale
Xbit30 A30 B30 G30 P30 Vdd Vss PG scale=scale
Xbit31 A31 B31 G31 P31 Vdd Vss PG scale=scale
Xbit32 A32 B32 G32 P32 Vdd Vss PG scale=scale
Xbit33 A33 B33 G33 P33 Vdd Vss PG scale=scale
Xbit34 A34 B34 G34 P34 Vdd Vss PG scale=scale
Xbit35 A35 B35 G35 P35 Vdd Vss PG scale=scale
Xbit36 A36 B36 G36 P36 Vdd Vss PG scale=scale
Xbit37 A37 B37 G37 P37 Vdd Vss PG scale=scale
Xbit38 A38 B38 G38 P38 Vdd Vss PG scale=scale
Xbit39 A39 B39 G39 P39 Vdd Vss PG scale=scale
Xbit40 A40 B40 G40 P40 Vdd Vss PG scale=scale
Xbit41 A41 B41 G41 P41 Vdd Vss PG scale=scale
Xbit42 A42 B42 G42 P42 Vdd Vss PG scale=scale
Xbit43 A43 B43 G43 P43 Vdd Vss PG scale=scale
Xbit44 A44 B44 G44 P44 Vdd Vss PG scale=scale
Xbit45 A45 B45 G45 P45 Vdd Vss PG scale=scale
Xbit46 A46 B46 G46 P46 Vdd Vss PG scale=scale
Xbit47 A47 B47 G47 P47 Vdd Vss PG scale=scale
Xbit48 A48 B48 G48 P48 Vdd Vss PG scale=scale
Xbit49 A49 B49 G49 P49 Vdd Vss PG scale=scale
Xbit50 A50 B50 G50 P50 Vdd Vss PG scale=scale
Xbit51 A51 B51 G51 P51 Vdd Vss PG scale=scale
Xbit52 A52 B52 G52 P52 Vdd Vss PG scale=scale
Xbit53 A53 B53 G53 P53 Vdd Vss PG scale=scale
Xbit54 A54 B54 G54 P54 Vdd Vss PG scale=scale
Xbit55 A55 B55 G55 P55 Vdd Vss PG scale=scale
Xbit56 A56 B56 G56 P56 Vdd Vss PG scale=scale
Xbit57 A57 B57 G57 P57 Vdd Vss PG scale=scale
Xbit58 A58 B58 G58 P58 Vdd Vss PG scale=scale
Xbit59 A59 B59 G59 P59 Vdd Vss PG scale=scale
Xbit60 A60 B60 G60 P60 Vdd Vss PG scale=scale
Xbit61 A61 B61 G61 P61 Vdd Vss PG scale=scale
Xbit62 A62 B62 G62 P62 Vdd Vss PG scale=scale
Xbit63 A63 B63 G63 P63 Vdd Vss PG scale=scale
Xbit64 A64 B64 G64 P64 Vdd Vss PG scale=scale

V_G0   G0 Cin 0
V_P0   P0 Vss 0

.ENDS PG64
