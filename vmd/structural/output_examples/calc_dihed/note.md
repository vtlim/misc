```
vmdt -e /home/limvt/connect/hpc/goto-tw/gitmisc/vmd/structural/analyzeDCD.tcl -args ../../00_reference/popc_t1pos.psf 50 ../../00_reference/popc_t1pos.pdb ../../win01/01/win01.01.dcd ../../win01/02/win01.02.dcd ../../win01/03/win01.03.dcd 
calc_dihed gbi1_win01.dat resname,GBI1,and,name,N4 resname,GBI1,and,name,C1 resname,GBI1,and,name,N2 resname,GBI1,and,name,C
python ../../polar_plot.py -i gbi1_win01.dat
```
