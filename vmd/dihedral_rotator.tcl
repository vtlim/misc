# __________________________________________________________________________________
#
# dihedral_rotator.tcl
#
# Purpose:          Rotate some dihedral angle in VMD.
# Usage:
#   source dihedral_rotator.tcl
#   set movesel [atomselect top "something"]
#   incr_dihedral molid $movesel ind1 ind2 angle_change
#
# Notes:
# - Angle change is the amount (in degrees) to rotate around bond ind1-ind2
# __________________________________________________________________________________

proc incr_dihedral {molid movesel ind1 ind2 delta} {

  ### Validate input.
  if {$ind1 == "" || $ind2 == ""} {
    puts "WARNING: Couldn't find one or more atoms for set_dihedral"
    return
  }

  ### Measure initial angle.
  set tmpmolid $molid

  ### Set both atoms of the central bond.
  set bsel1 [atomselect $tmpmolid "index $ind1"]
  set bsel2 [atomselect $tmpmolid "index $ind2"]

  ### Get degree to move by, and the move matrix.
  set mat [trans bond [lindex [$bsel1 get {x y z}] 0] [lindex [$bsel2 get {x y z}] 0] $delta deg]

  ### Move the selection by that matrix.
  $movesel move $mat
  $bsel1 delete
  $bsel2 delete

}
