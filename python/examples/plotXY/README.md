
# Examples for `plotXY.py`
For specific plot customizations (e.g., grid), see the git version of the `plotXY.py` script at the same time of the uploaded example.

Git commit: ad57548    

1. Basic plot
    * `python plotXY.py -i xy1.dat -x 'frame number' -y 'RMSD (A)' -l 'backbone;S1;S2;S3;S4' -o output1.png`
2. Running average over 100 data points
    * `python plotXY.py -i xy1.dat -m 100 -x 'time (ns)' -y 'RMSD (A)' -l 'backbone;S1;S2;S3;S4' -o output2.png`
3. Plot specific columns only
    * `python plotXY.py -i xy1.dat -c "2;3;4;5" -m 100 -x 'time (ns)' -y 'RMSD (A)' -l 'S1;S2;S3;S4' -o output3.png`

Git commit: 54120c9    
1. Separate input into 50 lines, plotted in 5 windows  
    * `python plotXY.py -i xy4.dat -g 50 -o output4.png`
