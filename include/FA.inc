******************** HSPICE FULL ADDER MODELING *********************
*
*   Mohammad Khoshroo - 810102441 
*   Spring 2026
*   AVLSI Course - by Dr. Vahdat
*   Standard MOSFET Model Name : nch , pch
*
*
.INC "basic_gates.inc"
*
****************** FULL ADDER Gate-Level .SUBCKT ********************

.SUBCKT FA A B Cin S Cout Vdd Vss 

Xxor1   A       B       xorAB   Vdd Vss XOR2_SYM
Xxor2   Cin     xorAB   S       Vdd Vss XOR2_SYM
Xnand1  Cin     xorAB   nandCin Vdd Vss NAND2
Xnand2  A       B       nandAB  Vdd Vss NAND2
Xnand3  nandAB  nandCin Cout    Vdd Vss NAND2

.ENDS FA

********************** NAND-Based XOR .SUBCKT ***********************

.SUBCKT XNAND in1 in2 out_xor out_nand Vdd Vss

$ out_nand (out1) = ~(in1 & in2)
$ out_xor  (out4) =   in1 ^ in2

Xnand1  in1     in2      out_nand  Vdd Vss NAND2
Xnand2  in1     out_nand out2      Vdd Vss NAND2
Xnand3  in2     out_nand out3      Vdd Vss NAND2
Xnand4  out2    out3     out_xor   Vdd Vss NAND2

.ENDS XNAND

******************** FULL ADDER NAND BASED .SUBCKT *****************

.SUBCKT FA_N A B Cin S Cout Vdd Vss

Xxor1   A       B               xorAB   nandAB      Vdd Vss XNAND
Xxor2   xorAB   Cin             S       nandmid     Vdd Vss XNAND
Xcout   nandAB  nandmid         Cout                Vdd Vss NAND2

.ENDS FA_N

*********************** MIRROR ADDER .SUBCKT ***********************

.SUBCKT FA_M A B Cin S Cout Vdd Vss

$ MINORITY GATE (Cout_bar)

MpA_propagate   x         A       Vdd      Vdd   pch   L='L'   W='2 * Wp_min'
MpB_propagate   x         B       Vdd      Vdd   pch   L='L'   W='2 * Wp_min'
MpC_propagate   Cout_bar  Cin     x        Vdd   pch   L='L'   W='2 * Wp_min'

MpA_kill        k         A       Vdd      Vdd   pch   L='L'   W='2 * Wp_min'
MpB_kill        Cout_bar  B       k        Vdd   pch   L='L'   W='2 * Wp_min'

MnA_propagate   y         A       Vss      Vss   nch   L='L'   W='2 * Wn_min'
MnB_propagate   y         B       Vss      Vss   nch   L='L'   W='2 * Wn_min'
MnC_propagate   Cout_bar  Cin     y        Vss   nch   L='L'   W='2 * Wn_min'

MnA_generate    g         A       Vss      Vss   nch   L='L'   W='2 * Wn_min'
MnB_generate    Cout_bar  B       g        Vss   nch   L='L'   W='2 * Wn_min'


$ SUM (S_bar)

MpA_and         and_u1    A       Vdd      Vdd   pch   L='L'   W='3 * Wp_min'
MpB_and         and_u2    B       and_u1   Vdd   pch   L='L'   W='3 * Wp_min'
MpC_and         S_bar     Cin     and_u2   Vdd   pch   L='L'   W='3 * Wp_min'

MpA_or          or_up     A       Vdd      Vdd   pch   L='L'   W='2 * Wp_min'
MpB_or          or_up     B       Vdd      Vdd   pch   L='L'   W='2 * Wp_min'
MpC_or          or_up     Cin     Vdd      Vdd   pch   L='L'   W='2 * Wp_min'
Mpco_or         S_bar     Cout_bar or_up   Vdd   pch   L='L'   W='2 * Wp_min'

MnA_and         and_d1    A       Vss      Vss   nch   L='L'   W='3 * Wn_min'
MnB_and         and_d2    B       and_d1   Vss   nch   L='L'   W='3 * Wn_min'
MnC_and         S_bar     Cin     and_d2   Vss   nch   L='L'   W='3 * Wn_min'

MnA_or          or_down   A       Vss      Vss   nch   L='L'   W='2 * Wn_min'
MnB_or          or_down   B       Vss      Vss   nch   L='L'   W='2 * Wn_min'
MnC_or          or_down   Cin     Vss      Vss   nch   L='L'   W='2 * Wn_min'
Mnco_or         S_bar     Cout_bar or_down Vss   nch   L='L'   W='2 * Wn_min'


$ INVS

Xinvc            Cout_bar  Cout   Vdd   Vss   INV
Xinvs            S_bar     S      Vdd   Vss   INV

.ENDS FA_M


***************** Transmission BASED ADDER .SUBCKT *****************

.SUBCKT FA_T A B Cin S Cout Vdd Vss

XinvA A   A_bar Vdd Vss INV
XinvC Cin C_bar Vdd Vss INV

$ Propagate TG
Xtg_p          B     P     A_bar  A     Vdd Vss TG
Xtg_pb         B     P_bar A      A_bar Vdd Vss TG

Mpp      A     B     P      Vdd  pch  L='L'  W='Wp_min'
Mnp      A_bar B     P      Vss  nch  L='L'  W='Wn_min'

Mpp_bar  A_bar B     P_bar  Vdd  pch  L='L'  W='Wp_min'
Mnp_bar  A     B     P_bar  Vss  nch  L='L'  W='Wn_min'

$ Sum TG
Xtg_s1  C_bar   S_bar P_bar  P         Vdd Vss TG
Xtg_s2  Cin     S_bar P      P_bar     Vdd Vss TG

$ Cout TG
Xtg_c1  C_bar   Cout_bar   P     P_bar Vdd Vss TG
Xtg_c2  A_bar   Cout_bar   P_bar P     Vdd Vss TG

XinvS  S_bar    S    Vdd Vss INV
XinvCo Cout_bar Cout Vdd Vss INV

.ENDS FA_T
