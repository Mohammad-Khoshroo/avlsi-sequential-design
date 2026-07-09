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
...
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

