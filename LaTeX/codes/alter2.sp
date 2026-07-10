
.ALTER hold_sweep

.PARAM t_tran = 20p              $ Transition time (Rise/Fall time)
.PARAM t_hold = 200p
.IC V(Q)=1.8 V(Q_bar)=0

VCLK CLK 0 PWL(0p 0 1000p 0 '1000p+t_tran' Vdd_val 2000p Vdd_val '2000p+t_tran' 0 4000p 0)
VD D 0 PWL(0p Vdd_val '1000p+t_hold' Vdd_val '1000p+t_hold+t_tran' 0 4000p 0)

.TRAN 1p 4000p UIC SWEEP t_hold 200p -100p -1p
.MEASURE TRAN Q_min MIN V(Q) FROM=800p TO=3500p

.OPTION POST= 2 PROBE RUNLVL=6
.PROBE V(D) V(Q) V(CLK)