********************* HSPICE FA GATES MODELING **********************
*
*   Mohammad Khoshroo - 810102441 
*   Spring 2026
*   AVLSI Course - by Dr. Vahdat
*   Thechnolegy - crn90g_2d5_lk_v1d2p1.lib (90nm)
*   Standard MOSFET Model Name : nch , pch
*   FA SIMULATION
*   TEMP(℃) 25
*   CORNER TT
*
**************************** PARAMETERS *****************************

.OPTION NOMOD
.LIB "../../../../include/crn90g_2d5_lk_v1d2p1.lib" TT
.INC "../../../../include/FA.inc"

.PARAM Vdd_val = 1                  $ supply-1 voltage
.PARAM Vss_val = 0                  $ supply-0 voltage
.PARAM beta = 2                     $ un/up
.PARAM L = 180n                     $ Channel length
.PARAM Wn_min = 1u                  $ Minimum Transistor width for n-types
.PARAM Wp_min = 'beta * Wn_min'     $ Minimum Transistor width for p-types


****************************** CIRCUIT ******************************

Xfull_adder A B Cin S Cout Vdd Vss FA     $ FA Under TEST/SIMULATION

************************* SIMULATION SETTING ************************

* Supplys Voltage Node
Vdd Vdd 0 DC 'Vdd_val'
Vss Vss 0 DC 'Vss_val'

.TRAN 0.01p 1000p SWEEP DATA= FA_TRANSISSION
.TEMP 25

VA   A   0 PWL(0p 'a_init*Vdd_val' 300p 'a_init*Vdd_val' 350p 'a_final*Vdd_val' 1000p 'a_final*Vdd_val')
VB   B   0 PWL(0p 'b_init*Vdd_val' 300p 'b_init*Vdd_val' 350p 'b_final*Vdd_val' 1000p 'b_final*Vdd_val')
VCin Cin 0 PWL(0p 'cin_init*Vdd_val' 300p 'cin_init*Vdd_val' 350p 'cin_final*Vdd_val' 1000p 'cin_final*Vdd_val')

.DATA  FA_TRANSISSION
+ a_init  a_final  b_init  b_final  cin_init  cin_final  is_fall_transition
+ 0       1        0       0        0         0          0    $ T1-w1: A changes (RISE), B=0, C=0
+ 1       0        0       0        0         0          1    $ T1-w2: A changes (FALL), B=0, C=0
+ 0       1        1       1        0         0          0    $ T2-w1: A changes (RISE), B=1, C=0
+ 1       0        1       1        0         0          1    $ T2-w2: A changes (FALL), B=1, C=0
+ 0       1        0       0        1         1          0    $ T3-w1: A changes (RISE), B=0, C=1
+ 1       0        0       0        1         1          1    $ T3-w2: A changes (FALL), B=0, C=1
+ 0       1        1       1        1         1          0    $ T4-w1: A changes (RISE), B=1, C=1
+ 1       0        1       1        1         1          1    $ T4-w2: A changes (FALL), B=1, C=1
+ 0       0        0       1        0         0          0    $ T5-w1: B changes (RISE), A=0, C=0
+ 0       0        1       0        0         0          1    $ T5-w2: B changes (FALL), A=0, C=0
+ 1       1        0       1        0         0          0    $ T6-w1: B changes (RISE), A=1, C=0
+ 1       1        1       0        0         0          1    $ T6-w2: B changes (FALL), A=1, C=0
+ 0       0        0       1        1         1          0    $ T7-w1: B changes (RISE), A=0, C=1
+ 0       0        1       0        1         1          1    $ T7-w2: B changes (FALL), A=0, C=1
+ 1       1        0       1        1         1          0    $ T8-w1: B changes (RISE), A=1, C=1
+ 1       1        1       0        1         1          1    $ T8-w2: B changes (FALL), A=1, C=1
+ 0       0        0       0        0         1          0    $ T9-w1: Cin changes (RISE), A=0, B=0
+ 0       0        0       0        1         0          1    $ T9-w2: Cin changes (FALL), A=0, B=0
+ 1       1        0       0        0         1          0    $ T10-w1: Cin changes (RISE), A=1, B=0
+ 1       1        0       0        1         0          1    $ T10-w2: Cin changes (FALL), A=1, B=0
+ 0       0        1       1        0         1          0    $ T11-w1: Cin changes (RISE), A=0, B=1
+ 0       0        1       1        1         0          1    $ T11-w2: Cin changes (FALL), A=0, B=1
+ 1       1        1       1        0         1          0    $ T12-w1: Cin changes (RISE), A=1, B=1
+ 1       1        1       1        1         0          1    $ T12-w2: Cin changes (FALL), A=1, B=1
.ENDDATA


* ===================================================================
* Virtual Trigger Node definition
* ===================================================================
Etrig trig_node 0 VOL='V(A,B) + V(B,Cin)'

* ===================================================================
* Raw Delay Measures (Let HSPICE output 'failed' for invalid edges)
* ===================================================================
.MEASURE TRAN tpLH_S    TRIG V(trig_node) VAL=0 RISE=1 TARG V(S)    VAL='0.5 * Vdd_val' RISE=1 TD=200p
.MEASURE TRAN tpHL_S    TRIG V(trig_node) VAL=0 FALL=1 TARG V(S)    VAL='0.5 * Vdd_val' FALL=1 TD=200p
.MEASURE TRAN tpLH_Cout TRIG V(trig_node) VAL=0 RISE=1 TARG V(Cout) VAL='0.5 * Vdd_val' RISE=1 TD=200p
.MEASURE TRAN tpHL_Cout TRIG V(trig_node) VAL=0 FALL=1 TARG V(Cout) VAL='0.5 * Vdd_val' FALL=1 TD=200p



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

* .ALTER  Run_SF_Corner
* .DEL LIB "../../utils/crn90g_2d5_lk_v1d2p1.lib" TT   $ Delete previous Corner Models
* .LIB "../../utils/crn90g_2d5_lk_v1d2p1.lib" SF       $ Add new Corner Models
* .OPTION POST= 2 PROBE RUNLVL=6
* .PROBE V(in) V(out)

* .ALTER  Run_FS_Corner
* .DEL LIB "../../utils/crn90g_2d5_lk_v1d2p1.lib" TT
* .LIB "../../utils/crn90g_2d5_lk_v1d2p1.lib" FS
* .OPTION POST= 2 PROBE RUNLVL=6
* .PROBE V(in) V(out)

* .ALTER  Run_SS_Corner
* .DEL LIB "../../utils/crn90g_2d5_lk_v1d2p1.lib" TT
* .LIB "../../utils/crn90g_2d5_lk_v1d2p1.lib" SS
* .OPTION POST= 2 PROBE RUNLVL=6
* .PROBE V(in) V(out)

* .ALTER  Run_FF_Corner
* .DEL LIB "../../utils/crn90g_2d5_lk_v1d2p1.lib" TT
* .LIB "../../utils/crn90g_2d5_lk_v1d2p1.lib" FF
* .OPTION POST= 2 PROBE RUNLVL=6
* .PROBE V(in) V(out)


* Each output file includes data for a fixed TEMP+Corner with beta parameter sweep

.END