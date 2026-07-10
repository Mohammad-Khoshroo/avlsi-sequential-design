********************* HSPICE FA GATES MODELING **********************
*
*   Mohammad Khoshroo - 810102441 
*   Spring 2026
*   AVLSI Course - by Dr. Vahdat
*   Thechnolegy - mm018.lib (180nm)
*   Standard MOSFET Model Name : nmos , pmos
*   FF SIMULATION
*   TEMP(℃) 25
*   CORNER TT
*
**************************** PARAMETERS *****************************

.OPTION NOMOD
.LIB "../../../../include/mm018.lib" TT
.INC "../../../../include/sequential_elements.inc"

.PARAM Vdd_val = 1.8                  $ supply-1 voltage
.PARAM Vss_val = 0                    $ supply-0 voltage
.PARAM beta = 2                       $ un/up
.PARAM L = 180n                       $ Channel length
.PARAM Wn_min = 220n                  $ Minimum Transistor width for n-types
.PARAM Wp_min = 'beta * Wn_min'       $ Minimum Transistor width for p-types


****************************** CIRCUIT ******************************

Xcircuit D CLK Q Q_bar Vdd Vss D_FF_POS     $ POS FF Under TEST/SIMULATION

************************* SIMULATION SETTING ************************

* Supplys Voltage Node
Vdd Vdd 0 DC 'Vdd_val'
Vss Vss 0 DC 'Vss_val'
.IC V(Q)="Vdd_val" V(Q_bar)="Vss_val"

VD   D   0 PWL(0p 0  200p 0  240p 'Vdd_val'  520p 'Vdd_val'  560p 0  1000p 0  1040p 'Vdd_val'  1320p 'Vdd_val'  1360p 0  2400p 0  2440p 'Vdd_val'  3200p 'Vdd_val')
VCLK CLK 0 PWL(0p 0  800p 0  840p 'Vdd_val'  1600p 'Vdd_val'  1640p 0  1800p 0  1840p 'Vdd_val'  2120p 'Vdd_val'  2160p 0  2600p 0  2640p 'Vdd_val'  2920p 'Vdd_val'  2960p 0  3200p 0)

*************************** OUTPUT SETTING **************************

.TRAN 1p 3200p UIC
.OPTION POST= 2 PROBE RUNLVL=6
.PROBE V(D) V(Q) V(CLK)

* Each output file includes data for a fixed TEMP+Corner with beta parameter sweep

.END