#
# center_at_origin.tcl
#
# Purpose: Center enter system at origin.
#
# Usage:
# [1] If in VMD interactive:
#     1. source center_at_origin.tcl
#     2. recenter
#        OR
#        recenter all 0 (where 'all' can be replaced by vmd selection text, and 0 can be replaced by molid)
#
# [2] If on command line:
#     1. vmd -dispdev none file.pdb -e ../../center_at_origin.tcl -args all 0
#
# Full path names for sourcing:
#   gpl: /DFS-L/DATA/mobley/limvt/gitmisc/vmd/center_at_origin.tcl
#   cas: /home/limvt/connect/greenplanet/goto-cluster/gitmisc/vmd/center_at_origin.tcl
#
# By:       Victoria T. Lim
# Version:  May 6 2019
#
# Notes:
# - May need to fix location of the dependency script (move_atoms.tcl)

source ../../move_atoms.tcl
#source /home/limvt/connect/greenplanet/goto-cluster/gitmisc/vmd/move_atoms.tcl

proc recenter { {seltext "all"} {molid 0} } {
    set sel [atomselect $molid $seltext]
    set oldcenter [measure center $sel]
    set vecmove [vecinvert $oldcenter]
    moveby $sel $vecmove
}

if {$argc > 0} {

    # grab molid argument
    if {$argc == 2} {
        set molid [lindex $argv 1]
    } else {
        set molid 0
    }

    set censel [lindex $argv 0]
    recenter $censel $molid
    animate write pdb centered_output.pdb sel [atomselect $molid all] $molid
    exit
}
