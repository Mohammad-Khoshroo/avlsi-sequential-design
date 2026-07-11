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

.TRAN 0.01p 1200.0p UIC SWEEP DATA=CIRCUIT
.TEMP 25

VE E 0 PWL(0p 'e_init*Vdd_val' 75.0p 'e_init*Vdd_val' 95.0p 'e_final*Vdd_val' 1200.0p 'e_final*Vdd_val')
VD D 0 PWL(0p 'd_init*Vdd_val' 75.0p 'd_init*Vdd_val' 95.0p 'd_final*Vdd_val' 1200.0p 'd_final*Vdd_val')

.DATA CIRCUIT
+ e_init e_final d_init d_final is_fall_transition
+ 0        1        0        0        0        $ T1-w1: E changes (RISE), D=0
+ 1        0        0        0        1        $ T1-w2: E changes (FALL), D=0
+ 0        1        1        1        0        $ T2-w1: E changes (RISE), D=1
+ 1        0        1        1        1        $ T2-w2: E changes (FALL), D=1
+ 0        0        0        1        0        $ T3-w1: D changes (RISE), E=0
+ 0        0        1        0        1        $ T3-w2: D changes (FALL), E=0
+ 1        1        0        1        0        $ T4-w1: D changes (RISE), E=1
+ 1        1        1        0        1        $ T4-w2: D changes (FALL), E=1
.ENDDATA

.MEASURE TRAN tpLH_Q_E TRIG V(E) VAL='0.5*Vdd_val' RISE=1 TD=65.0p TARG V(Q) VAL='0.5*Vdd_val' RISE=1
.MEASURE TRAN tpHL_Q_E TRIG V(E) VAL='0.5*Vdd_val' FALL=1 TD=65.0p TARG V(Q) VAL='0.5*Vdd_val' FALL=1
.MEASURE TRAN tpLH_Q_D TRIG V(D) VAL='0.5*Vdd_val' RISE=1 TD=65.0p TARG V(Q) VAL='0.5*Vdd_val' RISE=1
.MEASURE TRAN tpHL_Q_D TRIG V(D) VAL='0.5*Vdd_val' FALL=1 TD=65.0p TARG V(Q) VAL='0.5*Vdd_val' FALL=1

.OPTION POST= 2 PROBE RUNLVL=6
.PROBE V(D) V(Q) V(E)


************************************************************************* 

* .ALTER setup_sweep
* .PARAM t_tran = 20p              $ Transition time (Rise/Fall time)

* .PARAM t_setup = 300p
* .IC V(Q)=0 V(Q_bar)=1.8

* VE E 0 PWL(0p 0 1000p 0 '1000p+t_tran' Vdd_val 2000p Vdd_val '2000p+t_tran' 0 4000p 0)
* VD D 0 PWL(0p 0 '2000p-t_setup' 0 '2000p-t_setup+t_tran' Vdd_val 3500p Vdd_val '3500p+t_tran' 0 4000p 0)

* .TRAN 1p 4000p UIC SWEEP t_setup 300p 10p -1p
* .MEASURE TRAN Q_max MAX V(Q) FROM=1800p TO=3500p

* .OPTION POST= 2 PROBE RUNLVL=6
* .PROBE V(D) V(Q) V(E)


* *************************************************************************

* .ALTER hold_sweep

* .PARAM t_hold = 200p
* .IC V(Q)=1.8 V(Q_bar)=0

* VE E 0 PWL(0p 0 1000p 0 '1000p+t_tran' Vdd_val 2000p Vdd_val '2000p+t_tran' 0 4000p 0)
* VD D 0 PWL(0p Vdd_val '2000p+t_hold' Vdd_val '2000p+t_hold+t_tran' 0 4000p 0)

* .TRAN 1p 4000p UIC SWEEP t_hold 200p -100p -1p
* .MEASURE TRAN Q_min MIN V(Q) FROM=1800p TO=3500p

* .OPTION POST= 2 PROBE RUNLVL=6
* .PROBE V(D) V(Q) V(E)


.END