
# Usage: open vmd then call "source open_from_glob.tcl"

set flist [lsort -dictionary [glob */*coor]]
foreach f $flist {
  #mol new $f
  mol addfile $f
}
