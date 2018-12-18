
# ____________________________________________________________________________________
#
# permeation_traj.tcl
#
# Purpose:  Extract permeant z-position frames from input trajectories, then wrap output simulation in XY plane around permeant.
# Usage  :  vmdt -e permeation_traj.tcl -args [todo]
# Example:  vmdt -e permeation_traj.tcl -args [todo]
#           vmdt here stands for "vmd -dispdev none"
#
# Dependencies
#  1. move_atoms.tcl
#  2. pbchelper.tcl
#  3. pbctools VMD package
#
# TODO:
#  - remove need to specify sourcedir and hardcoded inpsf, indcds
#  - split this into two scripts, (1) main for extracting frames, (2) external tcl for wrapXY
#  - implement argument parsing
#  - add output information writing on psf, dcd's, skip, min, max, etc.
#
# Assumptions
#  - Only works on rectangular boxes
#  - Grid spacing can only be as fine as single decimal place
#  - Single decimal space also used to locate frames (must be consistent for dict keys)
#  - Wrap system around POPC center of mass
#  - Can create and delete tempwrapfiles subdirectory
#
# By:      Victoria T. Lim
# Version: Nov 9 2018
# ____________________________________________________________________________________

# import move_atoms.tcl and pbchelp.tcl
set sourcedir /dfs3/pub/limvt/gitmisc/vmd
source $sourcedir/move_atoms.tcl
source $sourcedir/pbchelp.tcl

# define the range (inclusive) for collective variable distance
set maxZ 40
set minZ -41
set spacing 1.0
set inpsf 00_reference/popc_t2pos.psf

# define solute atomselection for VMD
set sol "resname GBI2"
set high_to_low 1
set inskip 100

# translate system
proc sys_to_zero {all} {
    set to_be_moved [measure center $all]
    set to_be_moved [vecinvert $to_be_moved]
    moveby $all $to_be_moved
}

# define the grid in a dictionary where keys are grid point, values are if snapshot was found
# https://stackoverflow.com/questions/38435707/how-to-generate-sequence-of-numbers-in-tcl
for {set i 0} true {incr i} {
    set x [expr {$i*$spacing + $minZ}]
    if {$x > $maxZ} break
    set printable [format "%.1f" $x]
    dict set grid $printable 0
}
puts $grid

# read in system
mol new $inpsf
mol addfile win01/03/win01.03.dcd first 0 last -1 step $inskip waitfor all molid top
mol addfile win02/03/win02.03.dcd first 0 last -1 step $inskip waitfor all molid top
mol addfile win03/03/win03.03.dcd first 0 last -1 step $inskip waitfor all molid top
mol addfile win04/03/win04.03.dcd first 0 last -1 step $inskip waitfor all molid top
mol addfile win05/03/win05.03.dcd first 0 last -1 step $inskip waitfor all molid top
mol addfile win06/03/win06.03.dcd first 0 last -1 step $inskip waitfor all molid top
mol addfile win07/03/win07.03.dcd first 0 last -1 step $inskip waitfor all molid top
mol addfile win08/03/win08.03.dcd first 0 last -1 step $inskip waitfor all molid top
mol addfile win09/01/win09.01.dcd first 0 last -1 step $inskip waitfor all molid top
mol addfile win10/02/win10.02.dcd first 0 last -1 step $inskip waitfor all molid top

# wrap system around bilayer
package require pbctools
pbc wrap -centersel "resname POPC" -center com -compound res -all

# set selections
set wtt [atomselect top $sol]
set lip [atomselect top "lipid and name C21 C31"]
set all [atomselect top "all"]

# take notes
set outDataFile [open output.wrap w]
puts $outDataFile "# Input PSF: TODO\n# Input DCD, skip $inskip: TODO\n"
puts $outDataFile "# Distance (A) | Frame"
mkdir tempwrapfiles

# loop through frames to find snapshots of when solute has values at z-grid
set n [expr {[molinfo top get numframes]-1}]
for {set i 0} {$i < $n} {incr i} {

    # update frames and selections
    $wtt frame $i
    $lip frame $i
    $all frame $i

    # subtract z coords: (water) - (center of mass of lipids)
    set dist [expr {[lindex [measure center $wtt] 2] - [lindex [measure center $lip] 2]}]

    # pseudo-round by formatting to single decimal place
    set dist [format "%.1f" $dist]

    # see if that dist is one of the grid points
    if { [dict exists $grid $dist] && ![dict get $grid $dist] } {
        puts "=========== Writing out distance: $dist ==========="

        # note where this frame came from
        puts $outDataFile "$dist $i"

        # shift center of mass of system to origin
        sys_to_zero $all

        # write out temporary pdb file
        animate write pdb tempwrapfiles/$dist.pdb beg $i end $i skip 1 0

        # mark this grid as complete
        dict set grid $dist 1
    }
}

# delete trajectory (mol 0) now that we're done, and reload psf (mol 1)
mol delete 0
mol new $inpsf
set molid 1
# probably can make this part a fx bc repeated 2x
set wtt [atomselect $molid $sol]
set all [atomselect $molid "all"]

if {$high_to_low} {
    # reverse order the dictionary keys
    foreach k [lsort -real -decreasing [dict keys $grid]] {
        if {[dict get $grid $k]==1} {
            puts "=========== Reading in distance: $k ==========="
            mol addfile tempwrapfiles/$k.pdb waitfor all
        }
    }
} else {
    # read all frames back, in order that keys were added
    dict for {k v} $grid {
        if {$v==1} {
            puts "=========== Reading in distance: $k ==========="
            mol addfile tempwrapfiles/$k.pdb waitfor all
        }
    }
}

# loop over all frames to do wrapping
set n [expr {[molinfo 1 get numframes]}]
for {set i 0} {$i < $n} {incr i} {

    # update frame to get accurate selections/unit cell
    animate goto $i
    $wtt frame $i
    $all frame $i

    # get unit cell info
    # inspired by https://github.com/frobnitzem/pbctools/blob/master/pbcwrap.tcl
    # using procs from /home/limvt/local/lib/vmd/plugins/noarch/tcl/pbctools2.8/pbcset.tcl
    # (can't source pbcset directly)
    set cell [molinfo $molid get { a b c alpha beta gamma }]
    pbc_check_cell $cell
    set cell [pbc_vmd2namd $cell]
    set A [lindex $cell 0]
    set B [lindex $cell 1]
    set C [lindex $cell 2]
    set Ax [lindex $A 0]
    set By [lindex $B 1]
    set Cz [lindex $C 2]

    # compute coordinates for origin
    set origin {0 0 0}
    set com [measure center $wtt]
    set origin [vecadd $origin $com]
    # don't move the z origin (aka wrap in xy direction only)
    lset origin 2 0

    # wrap
    set wrapsel "all and (same residue as (%s))"
    set halfcell [vecscale 0.5 [list $Ax $By $Cz]]
    #puts "CENTER COORDS: $origin"
    #puts "half cell: $halfcell"
    set maxy [expr [lindex $origin 1] + [lindex $halfcell 1]]
    set miny [expr [lindex $origin 1] - [lindex $halfcell 1]]
    set maxx [expr [lindex $origin 0] + [lindex $halfcell 0]]
    set minx [expr [lindex $origin 0] - [lindex $halfcell 0]]

    moveby [atomselect $molid [format $wrapsel "y>=$maxy"] frame $i] [vecinvert $B]
    moveby [atomselect $molid [format $wrapsel "y<$miny"]  frame $i] $B
    moveby [atomselect $molid [format $wrapsel "x>=$maxx"] frame $i] [vecinvert $A]
    moveby [atomselect $molid [format $wrapsel "x<$minx"]  frame $i] $A

    sys_to_zero $all
}

animate write dcd test.dcd waitfor all 1
rm -r tempwrapfiles
close $outDataFile
exit

