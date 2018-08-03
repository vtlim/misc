# Purpose: Generate bunch of histograms from input xy data.
# Usage: First load data, then click
#    Window > commands > read > hist.com > replay
# http://ringo.ams.sunysb.edu/index.php/Xmgrace#Histogram

# generate histograms
HISTOGRAM (S0, MESH(-81000, -79800, 100), OFF, OFF)
HISTOGRAM (S1, MESH(-81000, -79800, 100), OFF, OFF)
HISTOGRAM (S2, MESH(-81000, -79800, 100), OFF, OFF)
HISTOGRAM (S3, MESH(-81000, -79800, 100), OFF, OFF)
HISTOGRAM (S4, MESH(-81000, -79800, 100), OFF, OFF)
HISTOGRAM (S5, MESH(-81000, -79800, 100), OFF, OFF)
HISTOGRAM (S6, MESH(-81000, -79800, 100), OFF, OFF)
HISTOGRAM (S7, MESH(-81000, -79800, 100), OFF, OFF)
HISTOGRAM (S8, MESH(-81000, -79800, 100), OFF, OFF)
HISTOGRAM (S9, MESH(-81000, -79800, 100), OFF, OFF)
HISTOGRAM (S10, MESH(-81000, -79800, 100), OFF, OFF)
HISTOGRAM (S11, MESH(-81000, -79800, 100), OFF, OFF)
HISTOGRAM (S12, MESH(-81000, -79800, 100), OFF, OFF)
HISTOGRAM (S13, MESH(-81000, -79800, 100), OFF, OFF)
HISTOGRAM (S14, MESH(-81000, -79800, 100), OFF, OFF)
HISTOGRAM (S15, MESH(-81000, -79800, 100), OFF, OFF)
# output histograms to files
WRITE G0.S16 FILE "temp16.dat"
WRITE G0.S17 FILE "temp17.dat"
WRITE G0.S18 FILE "temp18.dat"
WRITE G0.S19 FILE "temp19.dat"
WRITE G0.S20 FILE "temp20.dat"
WRITE G0.S21 FILE "temp21.dat"
WRITE G0.S22 FILE "temp22.dat"
WRITE G0.S23 FILE "temp23.dat"
WRITE G0.S24 FILE "temp24.dat"
WRITE G0.S25 FILE "temp25.dat"
WRITE G0.S26 FILE "temp26.dat"
WRITE G0.S27 FILE "temp27.dat"
WRITE G0.S28 FILE "temp28.dat"
WRITE G0.S29 FILE "temp29.dat"
WRITE G0.S30 FILE "temp30.dat"
WRITE G0.S31 FILE "temp31.dat"
# clear all data from program
KILL G0.S0
KILL G0.S1
KILL G0.S2
KILL G0.S3
KILL G0.S4
KILL G0.S5
KILL G0.S6
KILL G0.S7
KILL G0.S8
KILL G0.S9
KILL G0.S10
KILL G0.S11
KILL G0.S12
KILL G0.S13
KILL G0.S14
KILL G0.S15
KILL G0.S16
KILL G0.S17
KILL G0.S18
KILL G0.S19
KILL G0.S20
KILL G0.S21
KILL G0.S22
KILL G0.S23
KILL G0.S24
KILL G0.S25
KILL G0.S26
KILL G0.S27
KILL G0.S28
KILL G0.S29
KILL G0.S30
KILL G0.S31
# reread data back in to get rid of formatting
READ NXY "temp16.dat"
READ NXY "temp17.dat"
READ NXY "temp18.dat"
READ NXY "temp19.dat"
READ NXY "temp20.dat"
READ NXY "temp21.dat"
READ NXY "temp22.dat"
READ NXY "temp23.dat"
READ NXY "temp24.dat"
READ NXY "temp25.dat"
READ NXY "temp26.dat"
READ NXY "temp27.dat"
READ NXY "temp28.dat"
READ NXY "temp29.dat"
READ NXY "temp30.dat"
READ NXY "temp31.dat"
# recolor linse
S0  line color 1
S1  line color 2        
S2  line color 3 
S3  line color 4 
S4  line color 5 
S5  line color 6 
S6  line color 7 
S7  line color 8 
S8  line color 9 
S9  line color 10 
S10 line color 11  
S11 line color 12  
S12 line color 0  
S13 line color 1  
S14 line color 2  
S15 line color 3  
S16 line color 4  
AUTOSCALE
