***************** HSPICE Brant-Kung ADDER MODELING ***************
*
*   Mohammad Khoshroo - 810102441 
*   Spring 2026
*   AVLSI Course - by Dr. Vahdat
*   Standard MOSFET Model Name : nch , pch
*
.INC "BK.inc"
*
********************* 8-bit BRENT-KUNG ADDER *********************

.SUBCKT BKA8 
+ A8 A7 A6 A5 A4 A3 A2 A1 
+ B8 B7 B6 B5 B4 B3 B2 B1 Cin
+ S8 S7 S6 S5 S4 S3 S2 S1 Cout Vdd Vss scale=1

X_PG8 
+ A1 A2 A3 A4 A5 A6 A7 A8 
+ B1 B2 B3 B4 B5 B6 B7 B8 Cin 
+ G1 G2 G3 G4 G5 G6 G7 G8 
+ P1 P2 P3 P4 P5 P6 P7 P8 
+ G0 P0 Vdd Vss PG8 scale=scale

X_BK8 
+ G8 P8 
+ G7 P7 
+ G6 P6 
+ G5 P5 
+ G4 P4 
+ G3 P3 
+ G2 P2 
+ G1 P1 
+ G0 
+ C0 C1 C2 C3 C4 C5 C6 C7 
+ Cout Vdd Vss BK8 scale=scale

X_Sum1 P1 C0 S1 Vdd Vss XOR2_SYM scale=scale
X_Sum2 P2 C1 S2 Vdd Vss XOR2_SYM scale=scale
X_Sum3 P3 C2 S3 Vdd Vss XOR2_SYM scale=scale
X_Sum4 P4 C3 S4 Vdd Vss XOR2_SYM scale=scale
X_Sum5 P5 C4 S5 Vdd Vss XOR2_SYM scale=scale
X_Sum6 P6 C5 S6 Vdd Vss XOR2_SYM scale=scale
X_Sum7 P7 C6 S7 Vdd Vss XOR2_SYM scale=scale
X_Sum8 P8 C7 S8 Vdd Vss XOR2_SYM scale=scale

.ENDS BKA8
