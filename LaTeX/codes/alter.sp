
.ALTER setup_sweep
.PARAM t_tran = 20p              $ Transition time (Rise/Fall time)

.PARAM t_setup = 300p
.IC V(Q)=0 V(Q_bar)=1.8

VE E 0 PWL(0p 0 1000p 0 '1000p+t_tran' Vdd_val 2000p Vdd_val '2000p+t_tran' 0 4000p 0)
VD D 0 PWL(0p 0 '2000p-t_setup' 0 '2000p-t_setup+t_tran' Vdd_val 3500p Vdd_val '3500p+t_tran' 0 4000p 0)

.TRAN 1p 4000p UIC SWEEP t_setup 300p 10p -1p
.MEASURE TRAN Q_max MAX V(Q) FROM=1800p TO=3500p

.OPTION POST= 2 PROBE RUNLVL=6
.PROBE V(D) V(Q) V(E)