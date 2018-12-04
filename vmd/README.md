# Scripts for analysis in VMD

Last updated: Dec 3 2018

## Contents

1. `analyzeDCD.tcl`
    * Purpose:          Various functions for MD simulation analysis in VMD.
    * Orig. source:     `/beegfs/DATA/mobley/limvt/hv1/04_fep/analysis/structural/analyzeDCD.tcl`

2. `drawBox.tcl`
    * Purpose:          Draw guide boxes (filled or outline)
    * Orig. source:     `/beegfs/DATA/mobley/limvt/hv1/04_fep/analysis/fixChg/drawBox.tcl`

2. `label_backbone.tcl`
    * Purpose:          Set beta value of protein backbone, such as for imposing harmonic restraints during equilibration.

3. `move_atoms.tcl`
    * Purpose:          Translate atoms in system
    * Orig. source:     `/beegfs/DATA/mobley/limvt/hv1/08_permeate/water/try02_recdHill/move_atoms.tcl`

4. `pbchelp.tcl`
    * Purpose:          Helper procedures to go with `wrapXY.tcl`
    * Orig. source:     `/beegfs/DATA/mobley/limvt/hv1/08_permeate/water/try02_recdHill/pbchelp.tcl`

5. `wrapXY.tcl`
    * Purpose:          Wrap membrane in XY place around specified selection
    * Orig. source:     `/beegfs/DATA/mobley/limvt/hv1/08_permeate/water/try02_recdHill/wrapXY.tcl`


## Notes
Anywhere that lists `vmdt` in script header description is referring to my shorthand for `vmd -dispdev none`.

