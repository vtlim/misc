
# Purpose of the script: to take and wrap every nth frame for summary trajectory.
# Usage: change files, then "vmd -e file.tcl -args file.psf file.dcd"
# vmd -e viewWrap.tcl -args /pub/limvt/pmf/00_reference/chipot_box.psf /pub/limvt/pmf/06_abf/win06-constRatio/06/*dcd


# ========================== Variables ========================= #

set skip 10
set psf [lindex $argv 0]
set dcd [lindex $argv 1]

# =============================================================== #

#lappend auto_path /home/victoria/Documents/tempotools/libs
package require tempoUserVMD

mol new $psf
dopbc -file $dcd -frames 0:$skip:-1

display depthcue off
display projection Orthographic
