********************* HSPICE FA GATES MODELING **********************
*
*   Mohammad Khoshroo - 810102441 
*   Spring 2026
*   AVLSI Course - by Dr. Vahdat
*   Thechnolegy - mm018.lib (180nm)
*   D-LATCH TIMING CHARACTERIZATION (tsetup, thold, tdq)
*
**************************** PARAMETERS *****************************

.OPTION NOMOD
.LIB "../../../../include/mm018.lib" TT
.INC "../../../../include/sequential_elements.inc"

.PARAM Vdd_val = 1.8
.PARAM Vss_val = 0
.PARAM beta = 2
.PARAM L = 180n
.PARAM Wn_min = 220n
.PARAM Wp_min = 'beta * Wn_min'
.PARAM Vth = 'Vdd_val/2'         $ Threshold voltage for measurements
.PARAM t_tran = 20p              $ Transition time (Rise/Fall time)

****************************** CIRCUIT ******************************

Xcircuit D E Q Q_bar Vdd Vss D_Latch_NN

************************* SIMULATION SETTING ************************

Vdd Vdd 0 DC 'Vdd_val'
Vss Vss 0 DC 'Vss_val'


*************************** OUTPUT SETTING **************************

.ALTER tdq_tcq_measure

.IC V(Q)=0 V(Q_bar)=1.8
.TRAN 1p 4000p UIC

VD D 0 PWL(0p 0 200p 0 200p+t_tran Vdd_val 1200p Vdd_val 1200p+t_tran 0 4000p 0)
VE E 0 PWL(0p 0 1000p 0 1000p+t_tran Vdd_val 2000p Vdd_val 2000p+t_tran 0 4000p 0)

.MEASURE TRAN t_cq TRIG V(E) VAL='Vth' RISE=1 TARG V(Q) VAL='Vth' RISE=1
.MEASURE TRAN t_dq TRIG V(D) VAL='Vth' FALL=1 TARG V(Q) VAL='Vth' FALL=1

.OPTION POST= 2 PROBE RUNLVL=6
.PROBE V(D) V(Q) V(E)


************************************************************************* 

.ALTER setup_sweep

.DEL MEASURE t_cq t_dq

.PARAM t_setup = 300p
.IC V(Q)=0 V(Q_bar)=1.8

VE E 0 PWL(0p 0 1000p 0 1000p+t_tran Vdd_val 2000p Vdd_val 2000p+t_tran 0 4000p 0)
VD D 0 PWL(0p 0 '2000p-t_setup' 0 '2000p-t_setup+t_tran' Vdd_val 3500p Vdd_val 3500p+t_tran 0 4000p 0)

.TRAN 1p 4000p UIC SWEEP t_setup 300p 10p -1p
.MEASURE TRAN Q_max MAX V(Q) FROM=1800p TO=3500p

.OPTION POST= 2 PROBE RUNLVL=6
.PROBE V(D) V(Q) V(E)


*************************************************************************

.ALTER hold_sweep

.DEL MEASURE t_cq t_dq Q_max

.PARAM t_hold = 200p
.IC V(Q)=1.8 V(Q_bar)=0

VE E 0 PWL(0p 0 1000p 0 1000p+t_tran Vdd_val 2000p Vdd_val 2000p+t_tran 0 4000p 0)
VD D 0 PWL(0p Vdd_val '2000p+t_hold' Vdd_val '2000p+t_hold+t_tran' 0 4000p 0)

.TRAN 1p 4000p UIC SWEEP t_hold 200p -30p -1p
.MEASURE TRAN Q_min MIN V(Q) FROM=1800p TO=3500p

.OPTION POST= 2 PROBE RUNLVL=6
.PROBE V(D) V(Q) V(E)


.END