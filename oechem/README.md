# Overview
Various scripts related to OpenEye python toolkits.

# Contents

* `am1wib.py` - finds invertible nitrogens and sums the angles around each.  
   example: `python am1wib.py -i input.sdf -o output.dat -p barplot-angles.dat`

* `charge_mols.py` - adds charges to mols using ELF10 model from oequacpac.  
   example: `python charge_mols.py -i input.sdf -o output.mol2` 

* `combineSDF.py` - combines molecule data from multiple files into a single SDF file.  
   example: `python combineSDF.py -i 01_setup/initCoords/ -o fromVMD.sdf`

* `filter_by_atom.py` - identifies molecules with interesting atoms.  
   example: `python filter_by_atom.py -i MiniDrugBank_filter00.mol2 -o MiniDrugBank_filter00_atomic.mol2 -b 1 6 7 8 16`

* `plotMultSDF.py` - similar to plotSDF.py but can plot multiple lines from multiple SDF files.  
   example: `python plotMultSDF.py -i plot.in -o results_vac.eps`

* `plotSDF.py` - plots data from a particular SD tag from an SDF file with multiple conformers.  
   example: `python plotSDF.py -i hf.sdf -t 'QM Turbomole Final Opt. Energy (Har) HF/6-31G*'`

