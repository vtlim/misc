
# ============================================================== #
# analyzeDCD.tcl
#
# By:       Victoria T. Lim
# Purpose:  Analyze list of trajectories using RMSD, RMSF, water density, etc.
#
# Usage:
#  1. vmd -dispdev none -e file.tcl -args inpsf inskip inpdb indcd [indcd2 indcd3 ...]
#  2. [call some analysis function in VMD terminal/console, see documentation]
#
# Usage of imported functions only (if you already have a trajectory loaded):
#  1. Comment out the "mol new ... mol addfile" part of this code.
#  2. Call "source analyzeDCD.tcl" in the active VMD session.
#  3. Some functions may need you to set variables (dcdlist, etc.) to write output files.
#
# Full path names for sourcing:
#   - gpl: /beegfs/DATA/mobley/limvt/gitmisc/vmd/structural/analyzeDCD.tcl
#   - cas: /home/limvt/connect/hpc/goto-tw/gitmisc/vmd/structural/analyzeDCD.tcl
#
# VTL notes:
#   - Read in trajectory data before loading functions, else doesn't load properly in visual mode with GUI.
#   - Don't wrap outside of indiv functions. rmsd/rmsf refers to pdb to align; pdb may not have pbc params for wrap
#
# Last updated: Jan 22 2020
#
# ========================== Variables ========================= #

set inpsf [lindex $argv 0]
set inskip [lindex $argv 1]
set inpdb [lindex $argv 2]

for {set i 3} {$i < $argc} {incr i} {
    lappend dcdlist [lindex $argv $i]
}

# ========================== Load inputs ========================= #

# read in data
mol new $inpsf
mol addfile $inpdb        ;# mol 0 == mol top
foreach dcd $dcdlist {    ;# maybe alter the first step to read in if FEP bc 50 frames equil
    mol addfile $dcd first 0 last -1 step $inskip waitfor all
}

# ===================== Helper functions ======================== #

package require pbctools
set __before [info procs] ; # get list of avail functions before loading this script

atomselect macro hv1_backbone { protein and backbone and {{resid 100 to 125} or {resid 134 to 160} or {resid 168 to 191} or {resid 198 to 220}} }

proc average L {
    # ============================================================
    # Get average of some list of numbers. Used in other functions.
    # ============================================================
    expr ([join $L +])/[llength $L].
}


proc diff {before after} {
    # ============================================================
    # Extract differences from two lists. Used in this script to
    # list available analysis functions after loading trajectories.
    #
    # References
    #  - https://tinyurl.com/yccerb3k
    # ============================================================
    set result [list]
    foreach name $before {
        set procs($name) 1
    }
    foreach name $after {
        if { ![info exists procs($name)] } {
            lappend result $name
        }
    }
    return [lsort $result]
} ;# end of diff


proc align_backbone { {refmolid 0} } {
    # ============================================================
    # Align Hv1 protein by backbone of transmembrane regions.
    # All frames with molid of 0 will be aligned. The reference
    # can either be frame 0 of molid 0, or a different molid.
    # Used in functions: calc_rmsd_hv1, calc_rmsf_hv1, count_wat_z
    #
    # Arguments
    #  - refmolid : int
    #       Integer value of the VMD molecule ID to use as reference.
    #       Default is 0, meaning use the originally loaded PDB.
    #       Specify a value other than 0 if loading an additional diff PDB.
    # ============================================================

    set wrapmolid 0
    set all [atomselect 0 "all"]
    set compprot [atomselect 0 hv1_backbone]
    set refprot [atomselect $refmolid hv1_backbone frame 0]

    set num_steps [molinfo 0 get numframes]
    for {set frame 0} {$frame < $num_steps} {incr frame} {
        $compprot frame $frame
        $all frame $frame
        $all move [measure fit $compprot $refprot]
    }
} ;# end of align_backbone


proc wrap_only { {top_index 0} {wrap_sel "protein"} } {

    # wrap and ignore given pdb -- sometimes has error (a=0.000000 b=0.000000 c=0.000000)
    # this function DOES NOT ALIGN bc some calculations only rely on independent distances of each frame
    set n [molinfo $top_index get numframes]
    pbc wrap -molid $top_index -compound fragment -center com -centersel "$wrap_sel" -first 1 -last $n ;# zero-based index

    return $n
} ;# end of wrap_only


proc wrap_and_align {center_sel moltop} {
    # ============================================================
    # Wrap system in molid 0. Align using align_backbone function
    # to align around Hv1 backbone.
    # This function can be replaced or edited to align around
    # a different selection.
    #
    # Example usage
    # - wrap_and_align "protein" 0
    #
    # ============================================================

    # wrap but do not align
    set num_frames [wrap_only $moltop "$center_sel"]

    # align system AFTER wrapping
    puts "Aligning system by Hv1 transmembrane backbone..."
    align_backbone $moltop

    return $num_frames

} ;# end of wrap_and_align


# ===================== Analysis functions ====================== #


proc calc_rmsd_hv1 {outprefix {level segment} {gbi 0} {inpdb ""} } {
    # ============================================================
    # Measure RMSD for Hv1. System is aligned by transmembrane
    # backbone, then RMSD can be calculated over backbone,
    # each segment (S1-S4), or each residue.
    #
    # Arguments
    #  - outprefix : string
    #       Basename of the output files for .dat, .psf, .pdb
    #  - level : string
    #       Level of detail to get RMSD values. Options: backbone, segment, residue
    #       Default is on segment.
    #  - gbi : integer
    #       2GBI tautomer. 0=absent, 1=taut1, 2=taut2.
    #       Default is on absent.
    #       Specify 0 if inpdb has no ligand, else error "measure rmsd: selections must have the same number of atoms"
    #  - inpdb : string
    #      Name of PDB file for reference instead of other loaded PDB for reference.
    #      Default is to use already-loaded PDB as reference.
    # Returns
    #  - (nothing)
    # Example usage
    #  - calc_rmsd_hv1 rmsd_segmt_f-01 segment 1 file.pdb
    # Notes
    #  - Only choose the "residue" selection for a few trajectories
    #    max. All 40 FEP windows will kill the job.
    #  - Make sure to allocate enough memory (e.g., for segment selection
    #    of 40 windows) as an interactive job.
    # ============================================================
    global inpsf
    global dcdlist

    set moltop 0
    if {$inpdb != ""} {
        mol new $inpdb
        set moltop 1
    }

    # wrap around given selection, then align around hv1 backbone wrt moltop
    wrap_and_align "protein" $moltop

    # set groups for RMSD calculation
    puts "Defining groups for RMSD calculation..."
    lappend rgroup "hv1_backbone"

    # determine groups for level of detail for protein
    if {$level == "residue" || $level == "resid"} {
        for {set resid 88} {$resid < 231} {incr resid} {
            lappend rgroup "protein and backbone and resid $resid"
        }
    } elseif {$level == "segment"} {
        lappend rgroup "protein and backbone and {{resid 100 to 125}}"
        lappend rgroup "protein and backbone and {{resid 134 to 160}}"
        lappend rgroup "protein and backbone and {{resid 168 to 191}}"
        lappend rgroup "protein and backbone and {{resid 198 to 220}}"
    }

    # determine group for ligand if present
    if {$gbi == 1} {
        lappend rgroup "segname GBI1 and noh"
    } elseif {$gbi == 2} {
        lappend rgroup "segname GBI2 and noh"
    }

    # open file for writing output
    set outDataFile [open $outprefix.dat w]
    puts $outDataFile "# Data from files:\n#  $inpsf\n#  $dcdlist"
    puts $outDataFile "# Alignment reference: $inpdb\n"
    puts $outDataFile "# RMSD (Angstroms)"
    set header "# Win | TM bb"

    if {$level == "residue" || $level == "resid"} {
        for {set resid 88} {$resid < 231} {incr resid} {
          lappend allres $resid
        }
        set reslabel [join $allres "\t\t"]
        set header "$header | $reslabel"

    } elseif {$level == "segment"} {
        set header "$header | S1\t\tS2\t\tS3\t\tS4"
    }

    if {$gbi == 1 || $gbi == 2} {
        set header "$header\t\t2GBI"
    }
    puts $outDataFile $header

    # rmsd calculation
    puts "Calculating RMSD..."
    set num_steps [molinfo 0 get numframes]
    for {set frame 0} {$frame < $num_steps} {incr frame} {
        if {[expr $frame % 100 == 0]} {puts $frame}
        set curr_line "$frame\t"
        foreach x $rgroup {
            set sel0 [atomselect $moltop $x frame 0]
            set sel1 [atomselect 0 $x frame $frame]
            set rmsdsel [format "%.4f" [measure rmsd $sel1 $sel0]]
            set curr_line "$curr_line\t$rmsdsel"
        }
        puts $outDataFile $curr_line
    }
    close $outDataFile

} ;# end of calc_rmsd_hv1


proc calc_rmsf_hv1 {outprefix} {
    # ============================================================
    # Measure RMSF by residue for Hv1. VMD cannot measure RMSF for
    # group of atoms, so each residue uses dummy atom that is the
    # center of mass of the amino acid (with backbone, no hydrogens)
    #
    # Arguments
    #  - outprefix : string
    #       Basename of the output files for .dat, .psf, .pdb
    # Returns
    #  - (nothing)
    # Example usage
    #  - calc_rmsf_hv1 rmsf_hv1
    # References
    #  - rmsf uses average position of frames as reference, https://tinyurl.com/yawa8xjo
    #  - use of dummy atom, https://tinyurl.com/y9l2wkvk
    # ============================================================
    global inpsf
    global inpdb
    global dcdlist

    # open file for writing output
    set outDataFile [open $outprefix.dat w]
    puts $outDataFile "# Data from files:\n#  $inpsf\n#  $dcdlist\n"
    puts $outDataFile "# Res | RMSF (Angstroms)"

    # borrow some lone ion to use as dummy atom
    # check that this atom exists if you get syntax error below
    # atomselect: cannot parse selection text: atomselect3
    set dumid 58225
    puts "Aligning system by Hv1 transmembrane backbone..."
    align_backbone

    # rmsf calculation
    puts "Calculating RMSF..."
    for {set resid 88} {$resid < 231} {incr resid} {
        set whole [atomselect top "protein and resid $resid"]
        set group [atomselect top "protein and resid $resid and noh"]
        set dummy [atomselect top "index $dumid"]

        set num_steps [molinfo top get numframes]
        for {set frame 0} {$frame < $num_steps} {incr frame} {
            $whole frame $frame
            $group frame $frame
            $dummy frame $frame

            # measure crds of center of this noh-residue and set crds on dummy atom
            set xyz [measure center $group]
            $dummy set x [lindex $xyz 0]
            $dummy set y [lindex $xyz 1]
            $dummy set z [lindex $xyz 2]
        }

        # rmsf calculation over all frames
        set rmsf [measure rmsf $dummy]
        $whole set occupancy $rmsf
        puts $outDataFile "$resid\t$rmsf"

    }

    # write out rmsf info in occupancy column of a PDB file
    animate write pdb $outprefix.pdb beg 0 end 0 sel [atomselect top protein]
    animate write psf $outprefix.psf beg 0 end 0 sel [atomselect top protein]
    close $outDataFile


} ;# end of calc_rmsf_hv1


proc count_wat_z { outfile sel_z0 sel_z1 {inpdb ""} } {
    # ============================================================
    # Count number of waters from -z0 to +z1 coordinate.
    #
    # Arguments
    #  - outfile : string
    #      Name of the output file.
    #  - sel_z0 : string
    #      Text selection for z0, should be in the lower z plane
    #  - sel_z1 : string
    #      Text selection for z1, should be in the upper z plane
    #  - inpdb : string
    #      Name of PDB file for reference instead of other loaded PDB for reference.
    #      Default is to use already-loaded PDB as reference.
    # Returns
    #  - (nothing)
    # Example usage
    #  - count_wat_z waters-in-zrange.dat "protein and resid 223 and name CZ" "protein and resid 208 and name CZ"
    # References
    #  - http://www.ks.uiuc.edu/Research/vmd/mailing_list/vmd-l/23723.html
    # ============================================================
    set watlist [list]
    set sel_x0 "protein and resid 173 and name O"
    set sel_x1 "protein and resid 134 and name CA"
    set sel_y0 "protein and resid 124 and name O"
    set sel_y1 "protein and resid 148 and name C"

    set moltop 0
    if {$inpdb != ""} {
        mol new $inpdb
        set moltop 1
    }

    # wrap around given selection, then align around hv1 backbone wrt moltop
    set n [wrap_and_align "protein" $moltop]

    puts "Counting waters..."

    # define output file
    set outDataFile [open $outfile w]
    puts $outDataFile "# Frame | number of waters bt Z crds of two sels"

    # get reference Z coordinates
    set z0 [[atomselect $moltop $sel_z0 frame 0] get {z}]
    set z1 [[atomselect $moltop $sel_z1 frame 0] get {z}]
    puts $outDataFile "# Selection 1 (z=$z0): $sel_z0\n# Selection 2 (z=$z1): $sel_z1"

    # get box edges
    set x0 [[atomselect $moltop $sel_x0 frame 0] get {x}]
    set x1 [[atomselect $moltop $sel_x1 frame 0] get {x}]
    set y0 [[atomselect $moltop $sel_y0 frame 0] get {y}]
    set y1 [[atomselect $moltop $sel_y1 frame 0] get {y}]
    puts $outDataFile "# Edge 1 (x=$x0): $sel_x0\n# Edge 2 (x=$x1): $sel_x1\n# Edge 3 (y=$y0): $sel_y0\n# Edge 4 (y=$y1): $sel_y1"

    # loop over frames
    set wats [atomselect 0 "noh and waters and (z<$z1 and z>$z0) and (x<$x1 and x>$x0) and (y<$y1 and y>$y0)"]
    for {set i 0} {$i < $n} {incr i} {
        $wats frame $i
        $wats update
        set num [$wats num]
        lappend watlist $num
        puts $outDataFile "$i $num"
    }

    $wats delete
    puts $outDataFile "# --- Average over traj: [average $watlist]"
    close $outDataFile

} ;# end of count_wat_z


proc count_wat_near { outfile dist args } {
    # ============================================================
    # Count number of waters within $dist Angstroms of the input selection(s).
    # Specify selection with no spaces, but use commas for multiple words.
    # See example usage.
    #
    # Arguments
    #  - outfile : string
    #      Name of the output file.
    #  - dist : integer
    #      Number of Angstroms from selection to find waters.
    #  - inpdb : string(s)
    #      Variable number of VMD selections for which to count waters within $dist cutoff.
    #      Each selection is analyzed separately.
    # Returns
    #  - (nothing)
    # Example usage
    #  - count_wat_near waters-near-selections.dat 3 sidechain,and,resid,211 resname,GBI1
    # Notes
    #  - To specify selection, separate words with commas, not spaces. ex: protein,and,resid,112
    #  - Built and validated from ligCloseWat.tcl in postFEPvanilla analysis scripts (08-23-18)
    # ============================================================
    global inpsf
    global inskip
    global inpdb
    global dcdlist

    # translate the comma arglist to spaced vmd selections
    for {set i 0} {$i < [llength $args]} {incr i} {
       set prelig [lindex $args $i]
       lappend sellist [split $prelig {,}]
    }

    # wrap but do not align
    set num_steps [wrap_only 0 "protein"]

    # define output file
    set outDataFile [open $outfile w]
    #puts $outDataFile "# Number of waters (noh) within $dist Angstroms"
    puts $outDataFile "# Number of waters (noh) within $dist Angstroms"
    puts $outDataFile "# Input PSF: $inpsf\n# Input DCD, skip $inskip: $dcdlist\n"
    set header "# Frame"
    for {set i 0} {$i < [llength $sellist]} {incr i} {
        puts $outDataFile "# Selection $i: [lindex $sellist $i]"
        append header "\t$i"
    }
    puts $outDataFile "\n$header"

    # waters calculation
    puts "Counting waters..."
    for {set frame 0} {$frame < $num_steps} {incr frame} {
        if {[expr $frame % 100 == 0]} {puts $frame}
        set curr_line "$frame\t"
        foreach x $sellist {
            #set cw [atomselect 0 "noh and water within $dist of ($x and noh)" frame $frame]
            set cw [atomselect 0 "noh and water within $dist of $x" frame $frame]
            set num [$cw num]
            append curr_line "\t$num"
        }
        puts $outDataFile $curr_line
    }
    close $outDataFile

} ;# end of count_wat_near


proc count_hbonds { seltxt1 seltxt2 {outprefix "hbonds"} } {
    # ============================================================
    # Quantify number of hbonds from seltxt1 to seltxt2.
    # Make sure to WRAP TRAJECTORY before use. (not called here
    # in case of already wrapped trajectory from other analysis)
    #
    # Arguments
    #  - seltxt1: string
    #      VMD selection
    #  - seltxt2 : string
    #      VMD selection
    #  - outprefix : string
    #       Basename of the output files for .dat, -details.dat, .log
    #       Default is "hbonds".
    # Returns
    #  - (nothing)
    # Example usage
    #  - count_hbonds "resname GBI1" "protein and resid 211"
    # ============================================================
    package require hbonds

    global inpsf
    global inskip
    global inpdb
    global dcdlist
    puts "Counting hydrogen bonds..."

    # define atom selections
    set sel1 [atomselect top "$seltxt1"]
    set sel2 [atomselect top "$seltxt2"]

    # evaluate hbonds
    #hbonds -sel1 $sel1 -sel2 $sel2 -writefile yes -upsel yes -frames all -dist 3.5 -ang 40 -plot no -log ${outprefix}.log -outfile ${outprefix}.dat -type unique -detailout ${outprefix}-details.dat
    hbonds -sel1 $sel1 -sel2 $sel2 -writefile yes -upsel yes -frames all -dist 3.5 -ang 40 -plot no -log ${outprefix}.log -outfile ${outprefix}.dat

    # append trajectory information to output
    set outDataFile [open ${outprefix}.log a]
    puts $outDataFile "\n# Input PSF: $inpsf\n# Input DCD, skip $inskip: $dcdlist"
    puts $outDataFile "# Selection 1: $seltxt1"
    puts $outDataFile "# Selection 2: $seltxt2\n"
    close $outDataFile


} ;# end of count_hbonds


proc calc_dist { outfile sel0 sel1 {sel2 ""} {sel3 ""} } {
    # ============================================================
    # Measure distance of selection 1 to selection[2,3,...].
    #
    # Arguments
    #  - outfile : string
    #      Name of the output file.
    #  - sel0 : string
    #      Text selection for reference atom
    #  - sel1 : string
    #      Text selection for atom for which to measure distance to atom0
    #  - sel2 : string
    #      Text selection for atom for which to measure distance to atom0. Optional.
    #  - sel3 : string
    #      Text selection for atom for which to measure distance to atom0. Optional.
    # Returns
    #  - (nothing)
    # Example usage
    #  - calc_dist lip_to_211.dat "lipid and resid 149 and name N" "protein and resid 211 and name CA"
    # Notes
    #  - If calcDistances to match with colvars traj file, uncomment the first step0 line
    #  - If you get error: "measure center: bad weight sum, would cause divide by zero", double check selection language.
    # ============================================================
    global inpsf
    global inskip
    global inpdb
    global dcdlist
    puts "Calculating distances..."

    # wrap but do not align
    wrap_only 0 "protein"

    # define output file
    set outDataFile [open $outfile w]
    puts $outDataFile "# Input PSF: $inpsf\n# Input DCD, skip $inskip: $dcdlist\n"
    puts $outDataFile "# Selection 0: $sel0\n# Selection 1: $sel1"

    if {[info exists sel2]} {
      puts $outDataFile "# Selection 2: $sel2"
    }
    if {[info exists sel3]} {
      puts $outDataFile "# Selection 3: $sel3"
    }
    puts $outDataFile "\n# Frame | Distance from sel0 to all other selections (Angstrom)"

    # set atom selections
    set atom1 [[atomselect top "$sel0"] get index]
    set atom2 [[atomselect top "$sel1"] get index]
    if {[info exists sel2]} {set atom3 [[atomselect top "$sel2"] get index]}
    if {[info exists sel3]} {set atom4 [[atomselect top "$sel3"] get index]}

    # take measurements
    set dist1 [measure bond [list $atom1 $atom2] frame all]
    if {[info exists sel2]} {set dist2 [measure bond [list $atom1 $atom3] frame all]}
    if {[info exists sel3]} {set dist3 [measure bond [list $atom1 $atom4] frame all]}

    # write output
    for {set i 0} {$i < [llength $dist1]} {incr i} {
        if {[info exists dist3]} { puts $outDataFile "$i\t[lindex $dist1 $i]\t[lindex $dist2 $i]\t[lindex $dist3 $i]" } \
        elseif {[info exists dist2]} { puts $outDataFile "$i\t[lindex $dist1 $i]\t[lindex $dist2 $i]" } \
        else { puts $outDataFile "$i\t[lindex $dist1 $i]" }
    }
    close $outDataFile

} ;# end of calc_dist


proc calc_dihed { outfile sel0 sel1 sel2 sel3 } {
    # ============================================================
    # Measure dihedral angle of the given four atoms.
    #
    # Arguments
    #  - outfile : string
    #      Name of the output file.
    #  - sel0 : string
    #      Text selection for atom of dihedral angle
    #  - sel1 : string
    #      Text selection for atom of dihedral angle
    #  - sel2 : string
    #      Text selection for atom of dihedral angle
    #  - sel3 : string
    #      Text selection for atom of dihedral angle
    # Returns
    #  - (nothing)
    # Example usage
    #  - calc_dihed gbi1_win02.dat "resname GBI1 and name N4" "resname GBI1 and name C1" "resname GBI1 and name N2" "resname GBI1 and name C"
    # Notes
    #  - This proc assumes that the four atoms are on the same molecule, else you may require trajectory align and/or wrap.
    #  - If you get error: "measure center: bad weight sum, would cause divide by zero", double check selection language.
    # ============================================================
    global inpsf
    global inskip
    global inpdb
    global dcdlist
    puts "Calculating dihedral angle..."

    # define output file
    set outDataFile [open $outfile w]
    puts $outDataFile "# Input PSF: $inpsf\n# Input DCD, skip $inskip: $dcdlist\n"
    puts $outDataFile "# Atom selections: $sel0 $sel1 $sel2 $sel3"
    puts $outDataFile "\n# Frame | Dihedral angle (degrees)"

    # set atom selections
    set atom1 [[atomselect top "$sel0"] get index]
    set atom2 [[atomselect top "$sel1"] get index]
    set atom3 [[atomselect top "$sel2"] get index]
    set atom4 [[atomselect top "$sel3"] get index]

    # take measurements
    set dihedlist [measure dihed [list $atom1 $atom2 $atom3 $atom4] frame all]

    # write output
    for {set i 0} {$i < [llength $dihedlist]} {incr i} {
        set ang [lindex $dihedlist $i]
        if {$ang < 0} {set ang [expr {360+$ang}]}
        puts $outDataFile "$i\t$ang"
    }
    close $outDataFile

} ;# end of calc_dihed


proc calc_dens_wat { {watsel ""} {outprefix "watdens"} } {
    # ============================================================
    # Calculate volumetric density of water (or other given selection) over trajectory.
    #
    # Arguments
    #  - watsel : string
    #      Selection for reference atom
    #  - outprefix : string
    #       Basename of the output files for dx, psf, pdb. Default is "watdens".
    # Returns
    #  - (nothing)
    # Example usage
    #  - calc_dens_wat "name OH2 and within 10 of (protein and resid 112 185 211)" watdens_nearSel
    #  - calc_dens_wat "name OH2 and within 10 of protein" watdens
    #  - calc_dens_wat "name OH2 and within 10 of protein"
    #  - calc_dens_wat
    # Notes
    #  - Only feed this function WRAPPED TRAJECTORIES. Wrapping the traj before calling volmap in this function
    #    doesn't work since the density doesn't align with the simulation (e.g., water slabs are out of range
    #    of the density map). (see sumtraj.tcl script like used for nodes/edges analysis)
    #  - If you get error: "measure center: bad weight sum, would cause divide by zero", double check selection language.
    # ============================================================
    global inpsf
    global inskip
    global inpdb
    global dcdlist
    set moltop 0

    # set vmd selection for waters
    if {$watsel == ""} {
        set watsel "name OH2"
    }
    set wat [atomselect top "$watsel"]

    # DISCARD the input PDB bc not wrapped (a=0.000000 b=0.000000 c=0.000000); might skew volmap avg
    animate delete beg 0 end 0 skip 0 $moltop

    # generate the volumetric map
    puts "Counting waters..."
    volmap density $wat -allframes -combine avg -res 0.25 -mol $moltop -o $outprefix.dx -weight mass

    # write out corresponding psf/pdb of wrapped traj view with dx
    animate write pdb $outprefix.pdb beg 0 end 0 sel [atomselect $moltop all]
    animate write psf $outprefix.psf beg 0 end 0 sel [atomselect $moltop all]

    # append trajectory information to output
    set outDataFile [open $outprefix.dx a]
    puts $outDataFile "# Input PSF: $inpsf\n# Input DCD, skip $inskip: $dcdlist"
    puts $outDataFile "# Density selection: $watsel\n"
    close $outDataFile

    # alert message about reliability of results
    puts "\n\n\nFinished with calc_dens_wat. Results are only valid if a WRAPPED trajectory was input!\n"

} ;# end of calc_dens_wat


proc calc_sel_orient { seltxt0 seltxt1 {outprefix "selorient"} } {
    # ============================================================
    # Calculate vector direction of some selection relative to bilayer normal direction.
    #
    # Arguments
    #  - seltxt0 : string
    #       VMD selection text of the base of the vector
    #  - seltxt1 : string
    #       VMD selection text of the end (arrow) of the vector
    #  - outprefix : string
    #       Basename of the output files for dat file. Default is "selorient".
    # Returns
    #  - (nothing)
    # Example usage
    #  - calc_sel_orient "resname GBI1 and name C4" "resname GBI1 and name C" orient_gbi1
    #  - calc_sel_orient "resname GBI1 and name C4" "resname GBI1 and name C"
    # Notes
    #  - If you get error: "measure center: bad weight sum, would cause divide by zero", double check selection language.
    # ============================================================
    global inpsf
    global inskip
    global inpdb
    global dcdlist
    set moltop 0

    # set vmd selection for vector
    set sel0 [atomselect top "$seltxt0"]
    set sel1 [atomselect top "$seltxt1"]
    set whole [atomselect top all]

    # write trajectory information to output
    set outDataFile [open $outprefix.dat w]
    puts $outDataFile "# Input PSF: $inpsf\n# Input DCD, skip $inskip: $dcdlist"
    puts $outDataFile "# VMD selection tail: $seltxt0"
    puts $outDataFile "# VMD selection head: $seltxt1\n"

    set num_steps [molinfo 0 get numframes]
    for {set frame 0} {$frame < $num_steps} {incr frame} {
        # update selections to this frame number
        $whole frame $frame
        $sel0 frame $frame
        $sel1 frame $frame

        # get vector of the selections
        set tailpt [lindex [$sel0 get {x y z}] 0] ;# un-nest lists
        set headpt [lindex [$sel1 get {x y z}] 0]
        set selvec [vecsub $headpt $tailpt]

        # take unit vector
        set unitvec [vecnorm $selvec]

        # dot product against +z direction
        set overlap [vecdot $unitvec {0 0 1}]

        puts $outDataFile "$frame\t$overlap"
    }
    close $outDataFile

} ;# end of calc_sel_orient


proc get_com_z { seltxt {outfile "z_com.dat"} } {
    # ============================================================
    # For the input selection, get its center of mass Z position.
    # Make sure to WRAP TRAJECTORY before use. (not called here
    # in case of already wrapped trajectory from other analysis)
    #
    # Arguments
    #  - outfile : string
    #      Name of the output file
    #  - seltxt : string
    #      VMD selection
    # Returns
    #  - (nothing)
    # Example usage
    #  - get_com_z "resname HIF" z_com_npt01.dat
    # ============================================================
    global inpsf
    global dcdlist
    puts "Calculating center of mass z-coordinate..."

    # set and create vmd selection
    set comsel [atomselect top "$seltxt"]

    # optionally, set reference selection
    #set refsel [atomselect top hv1_backbone]
    set refsel [atomselect top "name C21 C31"]

    # open file for writing output
    set outDataFile [open $outfile w]
    puts $outDataFile "# Data from files:\n#  $inpsf\n#  $dcdlist\n"
    puts $outDataFile "# Frame | COM Z position (Angstroms)"

    # loop over frames
    set num_steps [molinfo 0 get numframes]
    for {set frame 0} {$frame < $num_steps} {incr frame} {
        if {[expr $frame % 100 == 0]} {puts $frame}
        set curr_line "$frame\t"

        # update selection to this frame
        $comsel frame $frame
        $refsel frame $frame

        # get center of mass z coordinate
        #set z_now [lindex [measure center "$comsel"] 2]
        set z_now [expr {[lindex [measure center $comsel] 2] - [lindex [measure center $refsel] 2]}]

        # write to file
        puts $outDataFile "$curr_line\t$z_now"
    }

    close $outDataFile

} ;# end of get_com_z




# =============================================================== #
set __after [info procs] ; # get list of avail functions after loading this script
puts "\n\n[pwd]\n\nCheck if trajectories are done loading with \"molinfo top get numframes\" then analyze. Available functions:\n[diff $__before $__after]\n\n"

