
# MD simulation analysis in VMD with `analyzeDCD.tcl`
Last updated: Jan 22 2020

## Notes:

1. `vmdt` is my alias for `vmd -dispdev none` for non-GUI loading of VMD.
2. Original `polar_plot.py` from <https://github.com/vtlim/Hv1/tree/master/04_fep/postFEPvanilla/analysis/6_dists>

## Available functions
See function documentation in case of updates to what is listed here.

| proc                  | usage                                         | purpose                       |
|-----------------------|-----------------------------------------------|-------------------------------|
| `average`             | `average $list` (internal use)                | average list of numbers       |
| `diff`                | internal use only                             | diff between two lists        |
| `align_backbone`      | `align_backbone $top_index`                   | align transmembrane of Hv1    | 
| `wrap_only`           | `wrap_only $top_index "protein"`              | wrap system without alignment |
| `wrap_and_align`      | `wrap_and_align "protein" $top_index`         | wrap and align Hv1 backbone   |  
| `calc_rmsd_hv1`       | `calc_rmsd_hv1 prefix level lig_idx file.pdb` | calculate Hv1 RMSD over traj  | 
| `calc_rmsf_hv1`       | `calc_rmsf_hv1 prefix`                        | calculate Hv1 RMSF over traj  |
| `count_wat_z`         | `count_wat_z outfile pre_z0 pre_z1 file.pdb`  | count num waters in [z0,z1]   |
| `count_wat_near`      | `count_wat_near outfile dist vmd,sel,phrase`  | count num waters near sel     |
| `count_hbonds`        | `count_hbonds pre_sel2 pre_sel1 outprefix`    | count hbonds between sels     |
| `calc_dist`           | `calc_dist outfile pre0 pre1`                 | calc dist from sel0 to sel1   |
| `calc_dihed`          | `calc_dihed outfile pre0 pre1 pre2 pre3`      | calc dihedral angle of 4 sels |
| `calc_dens_wat`       | `calc_dens_wat presel outprefix`              | calc volumetric density of sel|
| `calc_sel_orient`     | `calc_sel_orient presel0 presel1 outprefix`   | calc vec direction wrt +z     |
| `get_com_z`           | `get_com_z presel output.dat`                 | calculate selection COM       |


## Procedure

1. Load trajectories.
   ```
   vmdt -e analyzeDCD.tcl -args infile.psf 1 infile.pdb infile.dcd
   ```

2. Call some analysis function (see function-specific documentation). Examples:
   ```
   calc_rmsf_hv1 rmsf_hv1
   count_wat_z waters-in-zrange.dat protein,and,resid,159,and,name,CA protein,and,resid,118,and,name,CA
   ```

## Additional examples

* Loading a set of FEP trajectories into the same molecule ID
  ```
  vmdt -e analyzeDCD.tcl -args ../../00_main/18629-19_R211S.psf 1 ../../00_main/18629-19_R211S.pdb ../../FEP_F/lambda_01/alchemy01.dcd ../../FEP_F/lambda_02/alchemy02.dcd ../../FEP_F/lambda_03/alchemy03.dcd ../../FEP_F/lambda_04/alchemy04.dcd ../../FEP_F/lambda_05/alchemy05.dcd ../../FEP_F/lambda_06/alchemy06.dcd ../../FEP_F/lambda_07/alchemy07.dcd ../../FEP_F/lambda_08/alchemy08.dcd ../../FEP_F/lambda_09/alchemy09.dcd ../../FEP_F/lambda_10/alchemy10.dcd ../../FEP_F/lambda_11/alchemy11.dcd ../../FEP_F/lambda_12/alchemy12.dcd ../../FEP_F/lambda_13/alchemy13.dcd ../../FEP_F/lambda_14/alchemy14.dcd ../../FEP_F/lambda_15/alchemy15.dcd ../../FEP_F/lambda_16/alchemy16.dcd ../../FEP_F/lambda_17/alchemy17.dcd ../../FEP_F/lambda_18/alchemy18.dcd ../../FEP_F/lambda_19/alchemy19.dcd ../../FEP_F/lambda_20/alchemy20.dcd
  ```
