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
.LIB "../../../../../include/mm018.lib" TT
.INC "../../../../../include/pipe.inc"

.PARAM Vdd_val = 1.8
.PARAM Vss_val = 0
.PARAM L = 180n
.PARAM Wn_min = 220n
.PARAM Wp_min = '2 * Wn_min'

****************************** CIRCUIT ******************************

Xpipe A B C D CLK OUT_l Vdd Vss LATCH_PIPE_P2

************************* INPUT SOURCES (PWL) ***********************

Vdd Vdd 0 DC 'Vdd_val'
Vss Vss 0 DC 'Vss_val'

VCLK CLK 0 PULSE (0 1.8 0 0.02n 0.02n 4.98n 10n)

VA A 0 PWL (
+ 0ns     0
+ 75.4ns  0   75.5ns  1.8
+ 155.4ns 1.8 155.5ns 0
+ )

VB B 0 PWL (
+ 0ns     0
+ 35.4ns  0   35.5ns  1.8
+ 75.4ns  1.8 75.5ns  0
+ 115.4ns 0   115.5ns 1.8
+ 155.4ns 1.8 155.5ns 0
+ )

VC C 0 PWL (
+ 0ns     0
+ 15.4ns  0   15.5ns  1.8
+ 35.4ns  1.8 35.5ns  0
+ 55.4ns  0   55.5ns  1.8
+ 75.4ns  1.8 75.5ns  0
+ 95.4ns  0   95.5ns  1.8
+ 115.4ns 1.8 115.5ns 0
+ 135.4ns 0   135.5ns 1.8
+ 155.4ns 1.8 155.5ns 0
+ )

VD D 0 PWL (
+ 0ns     0
+ 5.4ns   0   5.5ns   1.8
+ 15.4ns  1.8 15.5ns  0
+ 25.4ns  0   25.5ns  1.8
+ 35.4ns  1.8 35.5ns  0
+ 45.4ns  0   45.5ns  1.8
+ 55.4ns  1.8 55.5ns  0
+ 65.4ns  0   65.5ns  1.8
+ 75.4ns  1.8 75.5ns  0
+ 85.4ns  0   85.5ns  1.8
+ 95.4ns  1.8 95.5ns  0
+ 105.4ns 0   105.5ns 1.8
+ 115.4ns 1.8 115.5ns 0
+ 125.4ns 0   125.5ns 1.8
+ 135.4ns 1.8 135.5ns 0
+ 145.4ns 0   145.5ns 1.8
+ 155.4ns 1.8 155.5ns 0
+ )


************************* SIMULATION SETTING ************************

.TRAN 0.05n 180n


*************************** OUTPUT SETTING **************************

.OPTION POST=2 PROBE 
.PROBE V(CLK) V(A) V(B) V(C) V(D) V(OUT_l)

.END
