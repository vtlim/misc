
# Purpose: label protein backbone atoms for restraining protein in new
#   simulation after minimization. E.g.,
#   (1) minimize, (2) reinitvels, (3) turn on and slowly scale down harmonic restraints on backbone atoms
#
# Usage:    vmdt -e file.tcl -args file.pdb
# By:       Victoria T. Lim
# Version:  Mar 1 2017


# ========================== Variables ========================= #

set pdb [lindex $argv 0]

# =============================================================== #

#lappend auto_path /home/victoria/Documents/tempotools/libs
#package require tempoUserVMD

mol new $pdb
set mark [atomselect top "backbone"]
$mark set beta 1
[atomselect top all] writepdb harm_const.cnst
exit


