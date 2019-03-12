
# Purpose: Open a bunch of molecules in VMD specifying them on the command line.
# Usage: vmd -e openManyMols.tcl -args file1 file2 file3 ...

for {set i 0} {$i < $argc} {incr i} {
    mol new [lindex $argv $i]
    }
