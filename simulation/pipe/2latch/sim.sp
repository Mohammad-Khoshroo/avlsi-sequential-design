********************* HSPICE FA GATES MODELING **********************
*
*   Mohammad Khoshroo - 810102441 
*   Spring 2026
*   AVLSI Course - by Dr. Vahdat
*   Thechnolegy - mm018.lib (180nm)
*   LATCH_PIPE Tc - MAX constraint
*
**************************** PARAMETERS *****************************

.OPTION NOMOD
.LIB "../../../include/mm018.lib" TT
.INC "../../../include/pipe.inc"

.PARAM Vdd_val = 1.8
.PARAM Vss_val = 0
.PARAM beta = 2
.PARAM L = 180n
.PARAM Wn_min = 220n
.PARAM Wp_min = 'beta * Wn_min'
.PARAM Vth = 'Vdd_val/2'         $ Threshold voltage for measurements
.PARAM t_tran = 20p              $ Transition time (Rise/Fall time)

****************************** CIRCUIT ******************************

* Changed REG_PIPE to LATCH_PIPE
Xcircuit A B C D CLK OUT Vdd Vss  LATCH_PIPE

************************* SIMULATION SETTING ************************

.PARAM Tc = 1500p        $ theory Minimmum Tc 
.PARAM T_init = 1000p    $ Initialization 

Vdd Vdd 0 DC 'Vdd_val'
Vss Vss 0 DC 'Vss_val'
 
VA A 0 DC 'Vdd_val' $ A = 1
VC C 0 DC 'Vdd_val' $ C = 1
VD D 0 DC 'Vss_val' $ D = 0

$ B ( 1 -> 0 ) arriving just before the rising edge at 5n
VB B 0 PWL(0 'Vdd_val' 4.9n 'Vdd_val' '4.9n+t_tran' 'Vss_val' '5n + Tc - t_tran' 'vss_val' '5n + Tc' 'vdd_val')

VCLK CLK 0 PWL(
+ 0 'vss_val'
+ 100p 'vss_val'
+ '100p+t_tran' 'Vdd_val'
+ 300p 'Vdd_val'
+ '300p+t_tran' 'vss_val'
+ 'T_init' 'vss_val'
+ 4n 'vss_val'
+ '4n + t_tran' 'vdd_val'
+ 4.2n 'vdd_val'
+ '4.2n + t_tran' 'vss_val'
$ ********************* SWEEP START AT 5ns *********************
+ 5n 'vss_val'
+ '5n + t_tran' 'vdd_val'
+ '5n + Tc/2 + t_tran' 'vdd_val'
+ '5n + Tc/2 + 2*t_tran' 'vss_val'
+ '5n + Tc + 2*t_tran' 'vss_val'
+ '5n + Tc + 3*t_tran' 'vdd_val'
+ '5n + 3/2*Tc + 3*t_tran' 'vdd_val'
+ '5n + 3/2*Tc + 4*t_tran' 'vss_val'
+ '5n + 2*Tc + 4*t_tran' 'vss_val'
+ '5n + 2*Tc + 5*t_tran' 'vdd_val'
+ '5n + 5/2*Tc + 5*t_tran' 'vdd_val'
+ '5n + 5/2*Tc + 6*t_tran' 'vss_val'
+ '5n + 3*Tc + 6*t_tran' 'vss_val'
+ )

*************************** OUTPUT SETTING **************************

.TRAN 1p 10n SWEEP Tc 1500p 1100p -1p 
.MEASURE TRAN Out_min MIN V(OUT) FROM=6n TO=8n

.OPTION POST=2 PROBE RUNLVL=6
.PROBE TRAN V(A) V(B) V(C) V(D) V(CLK) V(OUT) V(Xcircuit.A_l) V(Xcircuit.B_l) V(Xcircuit.C_l) V(Xcircuit.D_l) V(Xcircuit.comb_out)  V(Xcircuit.CLK_not)

.END
