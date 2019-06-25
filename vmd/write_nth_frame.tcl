
# Purpose:  Write every nth frame from a trajectory as a separate PDB file.
# Usage:    vmd -dispdev text -e write_nth_frame.tcl -args N prefix file.psf file.dcd [file2.dcd]
# Version:  June 24 2019


# ========================== Variables ========================= #

set inskip [lindex $argv 0]
set prefix [lindex $argv 1]
set inpsf  [lindex $argv 2]

set index 3
while {$index < [llength $argv]} {
    lappend dcdlist [lindex $argv $index]
    incr index 1
}

# =============================================================== #

# Load files
mol new $inpsf
foreach mydcd $dcdlist {
    mol addfile $mydcd first 0 last -1 step $inskip waitfor all molid top
}

# Create system selection
set sel [atomselect top all]

# Loop over every frame and write pdb
set n [expr {[molinfo top get numframes]}]
for {set i 0} {$i < $n} {incr i} {

    $sel frame $i
    animate write pdb ${prefix}_$i.pdb beg $i end $i skip 1 top
}

# Write out extracted information
set outDataFile [open ${prefix}_snapshots.dat a]
puts $outDataFile "\n# Date: [clock format [clock seconds]]\n# Dir:  [pwd]"
puts $outDataFile "# Input PSF: $inpsf\n# Input DCD, skip $inskip: $dcdlist"
close $outDataFile

exit


# =============================================================== #

