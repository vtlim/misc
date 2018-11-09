#!/usr/bin/env python

"""
Charge the input molecules using the ELF10 charging model in OpenEye.

Usage: python charge_mols.py -i inputfile.sdf -o outputfile.mol2

By: Victoria T. Lim

"""

import os, sys
import openeye.oechem as oechem
import openeye.oequacpac as oequacpac
import argparse


### ------------------- Script -------------------


def charge_mols(infile, outfile, reffile=None):

    ### Read in molecules
    ifs = oechem.oemolistream()
    if not ifs.open(infile):
        oechem.OEThrow.Warning("Unable to open %s for reading" % infile)
        return

    ### Open output file
    ofs = oechem.oemolostream()
    if not ofs.open(outfile):
        oechem.OEThrow.Fatal("Unable to open %s for writing" % outfile)

    ### Charge the molecules and write output
    if reffile is None:
        for mol in ifs.GetOEMols():
            if not oequacpac.OEAssignCharges(mol, oequacpac.OEAM1BCCELF10Charges()):
                oechem.OEThrow.Warning("Unable to charge mol {}".format(mol.GetTitle()))
            oechem.OEWriteConstMolecule(ofs, mol)
        ifs.close()
        ofs.close()
    else:
        ### Read in molecules
        rfs = oechem.oemolistream()
        if not rfs.open(reffile):
            oechem.OEThrow.Warning("Unable to open %s for reading" % reffile)
            return
        ### Set coordinates of desired molecule on the mol with charges
        for in_mol, ref_mol in zip(ifs.GetOEMols(), rfs.GetOEMols()):
            ref_mol.SetCoords(in_mol.GetCoords())
            oechem.OEWriteConstMolecule(ofs, ref_mol)
        ifs.close()
        ofs.close()




if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("-i", "--infile", required=True,
        help="Name of input SDF (or other) file.")
    parser.add_argument("-o", "--outfile", required=True,
        help="Name of output MOL2 file.")
    parser.add_argument("-r", "--reffile",
        help="Assign charges on input mols based on analogous reference file.")

    args = parser.parse_args()

    ### Check that input file exists.
    if not os.path.exists(args.infile):
        raise parser.error("Input file %s does not exist. Try again." % args.infile)
    ### Check that output file is not SDF
    if os.path.splitext(args.outfile)[1] == '.sdf':
        raise parser.error("SDF file cannot store charges in output.")

    charge_mols(args.infile, args.outfile, args.reffile)

