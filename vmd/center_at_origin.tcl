
# Purpose: Center enter system at origin.
# Usage:
# > While in VMD:
#       [0] might need to fix source location of move_atoms.tcl
#       [1] source center_at_origin.tcl
#       [2] recenter OR recenter all 0 (where all can be replaced by desired selection text, and 0 can be replaced by molid
# > On command line:
#       * TODO, not yet supported
# Full path names for sourcing:
#   gpl: /DFS-L/old_beegfs_data/mobley/limvt/gitmisc/vmd/center_at_origin.tcl
#   cas: /home/limvt/connect/greenplanet/goto-beegfs/gitmisc/vmd/center_at_origin.tcl
# By:       Victoria T. Lim
# Version:  Nov 29 2018

#source move_atoms.tcl
source /home/limvt/connect/greenplanet/goto-beegfs/gitmisc/vmd/move_atoms.tcl

proc recenter { {seltext "all"} {molid 0} } {
    set sel [atomselect $molid $seltext]
    set oldcenter [measure center $sel]
    set vecmove [vecinvert $oldcenter]
    moveby $sel $vecmove
}

