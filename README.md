
# Contents

* Directories
  * `examples/` 
  * `oechem/` 
  * `pca-viewer/` 
  * `vmd`
  * `xmgrace`

* Scripts
  * `awksed.py` - This script was used to process GROMACS `.top` files to add relevant lines for a dihedral restraint.  
    * Part of an example command:  
      `python awksed.py -i $i.top -s '[ moleculetype ]' -c 1 -a $'[ dihedral_restraints ]\n; atom1 a2 a3 a4 type=1 phi(ref) dphi kfactor\n4 3 2 8 1 $i 0 300\n' -r '$i' -p -1 -o $i.top`
  * `plotBar.py` - Customizable bar plots.
  * `plotXY.py` - This script takes an ASCII data file of an x-data column then 1+ y-data columns and plots y against x. Additional features:
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
