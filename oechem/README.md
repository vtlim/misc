# Overview
Various scripts related to OpenEye python toolkits.

# Contents

* `classifyN.py` - finds invertible nitrogens and sums the angles around each.  
   example: `python classifyN.py -f plan2pyr-222.sdf > angleResults.dat`

* `combineSDF.py` - combines molecule data from multiple files into a single SDF file.  
   example: `python combineSDF.py -i 01_setup/initCoords/ -o fromVMD.sdf`

* `plotMultSDF.py` - similar to plotSDF.py but can plot multiple lines from multiple SDF files.  
   example: `python plotMultSDF.py -i plot.in -o results_vac.eps`

* `plotSDF.py` - plots data from a particular SD tag from an SDF file with multiple conformers.  
   example: `python plotSDF.py -i hf.sdf -t 'QM Turbomole Final Opt. Energy (Har) HF/6-31G*'`
