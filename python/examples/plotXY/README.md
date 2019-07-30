
# Examples for `plotXY.py`
For specific plot customizations (e.g., grid), see the git version of the `plotXY.py` script at the same time of the uploaded example.

1. Basic plot [1]
    * `python plotXY.py -i xy1.dat -x 'frame number' -y 'RMSD (A)' -l 'backbone;S1;S2;S3;S4' -o output1.png`
2. Running average over 100 data points [1]
    * `python plotXY.py -i xy1.dat -m 100 -x 'time (ns)' -y 'RMSD (A)' -l 'backbone;S1;S2;S3;S4' -o output2.png`
3. Plot specific columns only [1]
    * `python plotXY.py -i xy1.dat -c "2;3;4;5" -m 100 -x 'time (ns)' -y 'RMSD (A)' -l 'S1;S2;S3;S4' -o output3.png`
4. Separate input into 50 lines, plotted in 5 windows. Script asks for manual entry for number of subplots (5). [2]
    * `python plotXY.py -i xy4.dat -g 50 -o output4.png`
5. Separate input into 5 lines, plotted in 1 window (interactive entry for number of subplots). [3]
    * `python ../../plotXY.py -i xy5.dat -g 5 -o output5.png -l "1;2;3;4;5" -x 'residue' -y 'RMSD ($\AA$)'`

Git commit:

[1] `ad57548`  
[2] `54120c9`
[3] `409ca99`
