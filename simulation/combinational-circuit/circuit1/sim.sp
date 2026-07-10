********************* HSPICE FA GATES MODELING **********************
*
*   Mohammad Khoshroo - 810102441 
*   Spring 2026
*   AVLSI Course - by Dr. Vahdat
*   Thechnolegy - mm018.lib (180nm)
*   Standard MOSFET Model Name : nmos , pmos
*   CIRCUIT SIMULATION
*   TEMP(℃) 25
*   CORNER TT
*
**************************** PARAMETERS *****************************

.OPTION NOMOD
.LIB "../../../include/mm018.lib" TT
.INC "../../../include/comb_circuit.inc"

.PARAM Vdd_val = 1.8                  $ supply-1 voltage
.PARAM Vss_val = 0                    $ supply-0 voltage
.PARAM beta = 2                       $ un/up
.PARAM L = 180n                       $ Channel length
.PARAM Wn_min = 220n                  $ Minimum Transistor width for n-types
.PARAM Wp_min = 'beta * Wn_min'       $ Minimum Transistor width for p-types


****************************** CIRCUIT ******************************

Xcircuit A B C D OUT Vdd Vss CIRCUIT     $ CIRCUIT Under TEST/SIMULATION

************************* SIMULATION SETTING ************************

* Supplys Voltage Node
Vdd Vdd 0 DC 'Vdd_val'
Vss Vss 0 DC 'Vss_val'

.TRAN 0.01p 700.0p SWEEP DATA=CIRCUIT_INPUT
.TEMP 25

VA A 0 PWL(0p 'a_init*Vdd_val' 75.0p 'a_init*Vdd_val' 125.0p 'a_final*Vdd_val' 700.0p 'a_final*Vdd_val')
VB B 0 PWL(0p 'b_init*Vdd_val' 75.0p 'b_init*Vdd_val' 125.0p 'b_final*Vdd_val' 700.0p 'b_final*Vdd_val')
VC C 0 PWL(0p 'c_init*Vdd_val' 75.0p 'c_init*Vdd_val' 125.0p 'c_final*Vdd_val' 700.0p 'c_final*Vdd_val')
VD D 0 PWL(0p 'd_init*Vdd_val' 75.0p 'd_init*Vdd_val' 125.0p 'd_final*Vdd_val' 700.0p 'd_final*Vdd_val')

.DATA CIRCUIT_INPUT
+ a_init a_final b_init b_final c_init c_final d_init d_final is_fall_transition
+ 0        1        0        0        0        0        0        0        0        $ T1-w1: A changes (RISE), B=0, C=0, D=0
+ 1        0        0        0        0        0        0        0        1        $ T1-w2: A changes (FALL), B=0, C=0, D=0
+ 0        1        1        1        0        0        0        0        0        $ T2-w1: A changes (RISE), B=1, C=0, D=0
+ 1        0        1        1        0        0        0        0        1        $ T2-w2: A changes (FALL), B=1, C=0, D=0
+ 0        1        0        0        1        1        0        0        0        $ T3-w1: A changes (RISE), B=0, C=1, D=0
+ 1        0        0        0        1        1        0        0        1        $ T3-w2: A changes (FALL), B=0, C=1, D=0
+ 0        1        1        1        1        1        0        0        0        $ T4-w1: A changes (RISE), B=1, C=1, D=0
+ 1        0        1        1        1        1        0        0        1        $ T4-w2: A changes (FALL), B=1, C=1, D=0
+ 0        1        0        0        0        0        1        1        0        $ T5-w1: A changes (RISE), B=0, C=0, D=1
+ 1        0        0        0        0        0        1        1        1        $ T5-w2: A changes (FALL), B=0, C=0, D=1
+ 0        1        1        1        0        0        1        1        0        $ T6-w1: A changes (RISE), B=1, C=0, D=1
+ 1        0        1        1        0        0        1        1        1        $ T6-w2: A changes (FALL), B=1, C=0, D=1
+ 0        1        0        0        1        1        1        1        0        $ T7-w1: A changes (RISE), B=0, C=1, D=1
+ 1        0        0        0        1        1        1        1        1        $ T7-w2: A changes (FALL), B=0, C=1, D=1
+ 0        1        1        1        1        1        1        1        0        $ T8-w1: A changes (RISE), B=1, C=1, D=1
+ 1        0        1        1        1        1        1        1        1        $ T8-w2: A changes (FALL), B=1, C=1, D=1
+ 0        0        0        1        0        0        0        0        0        $ T9-w1: B changes (RISE), A=0, C=0, D=0
+ 0        0        1        0        0        0        0        0        1        $ T9-w2: B changes (FALL), A=0, C=0, D=0
+ 1        1        0        1        0        0        0        0        0        $ T10-w1: B changes (RISE), A=1, C=0, D=0
+ 1        1        1        0        0        0        0        0        1        $ T10-w2: B changes (FALL), A=1, C=0, D=0
+ 0        0        0        1        1        1        0        0        0        $ T11-w1: B changes (RISE), A=0, C=1, D=0
+ 0        0        1        0        1        1        0        0        1        $ T11-w2: B changes (FALL), A=0, C=1, D=0
+ 1        1        0        1        1        1        0        0        0        $ T12-w1: B changes (RISE), A=1, C=1, D=0
+ 1        1        1        0        1        1        0        0        1        $ T12-w2: B changes (FALL), A=1, C=1, D=0
+ 0        0        0        1        0        0        1        1        0        $ T13-w1: B changes (RISE), A=0, C=0, D=1
+ 0        0        1        0        0        0        1        1        1        $ T13-w2: B changes (FALL), A=0, C=0, D=1
+ 1        1        0        1        0        0        1        1        0        $ T14-w1: B changes (RISE), A=1, C=0, D=1
+ 1        1        1        0        0        0        1        1        1        $ T14-w2: B changes (FALL), A=1, C=0, D=1
+ 0        0        0        1        1        1        1        1        0        $ T15-w1: B changes (RISE), A=0, C=1, D=1
+ 0        0        1        0        1        1        1        1        1        $ T15-w2: B changes (FALL), A=0, C=1, D=1
+ 1        1        0        1        1        1        1        1        0        $ T16-w1: B changes (RISE), A=1, C=1, D=1
+ 1        1        1        0        1        1        1        1        1        $ T16-w2: B changes (FALL), A=1, C=1, D=1
+ 0        0        0        0        0        1        0        0        0        $ T17-w1: C changes (RISE), A=0, B=0, D=0
+ 0        0        0        0        1        0        0        0        1        $ T17-w2: C changes (FALL), A=0, B=0, D=0
+ 1        1        0        0        0        1        0        0        0        $ T18-w1: C changes (RISE), A=1, B=0, D=0
+ 1        1        0        0        1        0        0        0        1        $ T18-w2: C changes (FALL), A=1, B=0, D=0
+ 0        0        1        1        0        1        0        0        0        $ T19-w1: C changes (RISE), A=0, B=1, D=0
+ 0        0        1        1        1        0        0        0        1        $ T19-w2: C changes (FALL), A=0, B=1, D=0
+ 1        1        1        1        0        1        0        0        0        $ T20-w1: C changes (RISE), A=1, B=1, D=0
+ 1        1        1        1        1        0        0        0        1        $ T20-w2: C changes (FALL), A=1, B=1, D=0
+ 0        0        0        0        0        1        1        1        0        $ T21-w1: C changes (RISE), A=0, B=0, D=1
+ 0        0        0        0        1        0        1        1        1        $ T21-w2: C changes (FALL), A=0, B=0, D=1
+ 1        1        0        0        0        1        1        1        0        $ T22-w1: C changes (RISE), A=1, B=0, D=1
+ 1        1        0        0        1        0        1        1        1        $ T22-w2: C changes (FALL), A=1, B=0, D=1
+ 0        0        1        1        0        1        1        1        0        $ T23-w1: C changes (RISE), A=0, B=1, D=1
+ 0        0        1        1        1        0        1        1        1        $ T23-w2: C changes (FALL), A=0, B=1, D=1
+ 1        1        1        1        0        1        1        1        0        $ T24-w1: C changes (RISE), A=1, B=1, D=1
+ 1        1        1        1        1        0        1        1        1        $ T24-w2: C changes (FALL), A=1, B=1, D=1
+ 0        0        0        0        0        0        0        1        0        $ T25-w1: D changes (RISE), A=0, B=0, C=0
+ 0        0        0        0        0        0        1        0        1        $ T25-w2: D changes (FALL), A=0, B=0, C=0
+ 1        1        0        0        0        0        0        1        0        $ T26-w1: D changes (RISE), A=1, B=0, C=0
+ 1        1        0        0        0        0        1        0        1        $ T26-w2: D changes (FALL), A=1, B=0, C=0
+ 0        0        1        1        0        0        0        1        0        $ T27-w1: D changes (RISE), A=0, B=1, C=0
+ 0        0        1        1        0        0        1        0        1        $ T27-w2: D changes (FALL), A=0, B=1, C=0
+ 1        1        1        1        0        0        0        1        0        $ T28-w1: D changes (RISE), A=1, B=1, C=0
+ 1        1        1        1        0        0        1        0        1        $ T28-w2: D changes (FALL), A=1, B=1, C=0
+ 0        0        0        0        1        1        0        1        0        $ T29-w1: D changes (RISE), A=0, B=0, C=1
+ 0        0        0        0        1        1        1        0        1        $ T29-w2: D changes (FALL), A=0, B=0, C=1
+ 1        1        0        0        1        1        0        1        0        $ T30-w1: D changes (RISE), A=1, B=0, C=1
+ 1        1        0        0        1        1        1        0        1        $ T30-w2: D changes (FALL), A=1, B=0, C=1
+ 0        0        1        1        1        1        0        1        0        $ T31-w1: D changes (RISE), A=0, B=1, C=1
+ 0        0        1        1        1        1        1        0        1        $ T31-w2: D changes (FALL), A=0, B=1, C=1
+ 1        1        1        1        1        1        0        1        0        $ T32-w1: D changes (RISE), A=1, B=1, C=1
+ 1        1        1        1        1        1        1        0        1        $ T32-w2: D changes (FALL), A=1, B=1, C=1
.ENDDATA

.MEASURE TRAN tpLH_out_A TRIG V(A) VAL='0.5*Vdd_val' RISE=1 TD=65.0p TARG V(out) VAL='0.5*Vdd_val' RISE=1
.MEASURE TRAN tpHL_out_A TRIG V(A) VAL='0.5*Vdd_val' FALL=1 TD=65.0p TARG V(out) VAL='0.5*Vdd_val' FALL=1
.MEASURE TRAN tpLH_out_B TRIG V(B) VAL='0.5*Vdd_val' RISE=1 TD=65.0p TARG V(out) VAL='0.5*Vdd_val' RISE=1
.MEASURE TRAN tpHL_out_B TRIG V(B) VAL='0.5*Vdd_val' FALL=1 TD=65.0p TARG V(out) VAL='0.5*Vdd_val' FALL=1
.MEASURE TRAN tpLH_out_C TRIG V(C) VAL='0.5*Vdd_val' RISE=1 TD=65.0p TARG V(out) VAL='0.5*Vdd_val' RISE=1
.MEASURE TRAN tpHL_out_C TRIG V(C) VAL='0.5*Vdd_val' FALL=1 TD=65.0p TARG V(out) VAL='0.5*Vdd_val' FALL=1
.MEASURE TRAN tpLH_out_D TRIG V(D) VAL='0.5*Vdd_val' RISE=1 TD=65.0p TARG V(out) VAL='0.5*Vdd_val' RISE=1
.MEASURE TRAN tpHL_out_D TRIG V(D) VAL='0.5*Vdd_val' FALL=1 TD=65.0p TARG V(out) VAL='0.5*Vdd_val' FALL=1



* ===================================================================
* Output Voltage Level (Vo)

.MEASURE TRAN VOH_val MAX V(out)
.MEASURE TRAN VOL_val MIN V(out)

* ===================================================================
* Power (P)

.MEASURE TRAN P_avg AVG POWER                       $ Average Power
.MEASURE TRAN P_max MAX POWER                       $ Maximum (Peak) Power
.MEASURE TRAN PDP PARAM = 'P_avg * tp_global_max'   $ Power-Delay Product (PDP)

* ===================================================================
* Current (I)

.MEASURE TRAN I_avg AVG  I(Vdd)
.MEASURE TRAN I_peak MIN I(Vdd)

*************************** OUTPUT SETTING **************************

.OPTION POST= 2 PROBE RUNLVL=6
.PROBE V(in) V(out)

* Each output file includes data for a fixed TEMP+Corner with beta parameter sweep

.END