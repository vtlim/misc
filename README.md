
# Contents

This file last updated: Nov 9 2018  

* Directories
  * `examples/` 
  * `oechem/` 
  * `pca-viewer/` 
  * `vmd/`
  * `xmgrace/`

* Scripts
  * `awksed.py` - Example application to process GROMACS `.top` files to add lines for dihedral restraint.  
    * Example:  
      `python awksed.py -i $i.top -s '[ moleculetype ]' -c 1 -a $'[ dihedral_restraints ]\n; atom1 a2 a3 a4 type=1 phi(ref) dphi kfactor\n4 3 2 8 1 $i 0 300\n' -r '$i' -p -1 -o $i.top`
  * `column_avg.py` 
  * `column_sum.py` 
  * `plotBar.py` - Customizable bar plots.
  * `plotScatter.py`
  * `plotXY.py` - Generates XY line plots from input ASCII data file of one `x` column and one or more `y` columns. This script can:
    * Subsample based on correlation time
    * Subsample based on running averages
    * Take in file of uncertainties to plot error bars
    * Separate a long xy data series into many line plots

* High-level view of contents
```
.
├── awksed.py
├── column_avg.py
├── column_sum.py
├── examples
│   ├── column_avg
│   ├── column_sum
│   ├── plotBar
│   ├── plotScatter
│   └── plotXY
├── oechem
│   ├── am1wib.py
│   ├── charge_mols.py
│   ├── combineSDF.py
│   ├── examples
│   ├── plotMultSDF.py
│   ├── plotSDF.py
│   └── README.md
├── openTabs.sh
├── pca-viewer
├── plotBar.py
├── plotScatter.py
├── plotXY.py
├── README.md
├── vmd
│   ├── drawBox.tcl
│   ├── move_atoms.tcl
│   ├── pbchelp.tcl
│   ├── README.md
│   └── wrapXY.tcl
└── xmgrace
    ├── add2.com
    ├── hist.com
    ├── README.md
    ├── runavg2.com
    ├── view2.par
    └── view2runavg.par
```
