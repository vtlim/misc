#!/usr/bin/env python

"""
Purpose:    Filter an input list of molecules to find ones with interesting atoms.
By:         Victoria T. Lim
Version:    Dec 20 2018
Example:    python filter_by_atom.py -i MiniDrugBank_filter00.mol2 -o MiniDrugBank_filter00_atomic.mol2 -b 1 6 7 8 16

"""

import openeye.oechem as oechem

def filter_by_atom(infile, outfile, boring_list):

    ### Read in molecules
    ifs = oechem.oemolistream()
    if not ifs.open(infile):
        oechem.OEThrow.Warning("Unable to open %s for reading" % infile)
        return

    ### Open output file
    ofs = oechem.oemolostream()
    if not ofs.open(outfile):
        oechem.OEThrow.Fatal("Unable to open %s for writing" % outfile)

    ### Go through all molecules
    for mol in ifs.GetOEMols():
        save_mol = False
        for atom in mol.GetAtoms():
            if atom.GetAtomicNum() not in boring_list:
                save_mol = True
        if save_mol:
            oechem.OEWriteConstMolecule(ofs, mol)
    ifs.close()
    ofs.close()

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()

    parser.add_argument("-i", "--infile", required=True,
        help="Name of input molecules file.")
    parser.add_argument("-o", "--outfile", required=True,
        help="Name of output molecules file.")
    parser.add_argument("-b", "--boring_list", nargs='*', type=int,
        help="Look for atomic numbers outside of this list")

    args = parser.parse_args()
    filter_by_atom(args.infile, args.outfile, args.boring_list)

