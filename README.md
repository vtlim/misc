
# Contents
* pca-viewer/   (VTL description here)
* `awksed.py`   This script was used to process GROMACS `.top` files to add relevant lines for a dihedral restraint.
Part of an example command: `python awksed.py -i $i.top -s '[ moleculetype ]' -c 1 -a $'[ dihedral_restraints ]\n; atom1 a2 a3 a4 type=1 phi(ref) dphi kfactor\n4 3 2 8 1 $i 0 300\n' -r '$i' -p -1 -o $i.top`
* `xyPlot.py`   This script takes an ASCII data file of an x-data column then N y-data columns (N>=1) and plots y against x. Can also subsample based on correlation times or take running averages of the data.
