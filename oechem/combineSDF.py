#!/usr/bin/env python

# Purpose:  Combine multiple molecular structure files into a single SDF file.
# By:       Victoria T. Lim
# Version:  Dec 10 2018


import os, sys, glob
import openeye.oechem as oechem


# --------------------------- Main Function ------------------------- #

def combineSDF(infiles, ftype, outfile):

    ### Glob for input files to combine.
    ext = '*.'+ftype
    molfiles = glob.glob(os.path.join(infiles, ext))

    ### Open output file to write molecules.
    ofs = oechem.oemolostream()
    if os.path.exists(outfile) and os.path.getsize(outfile) > 10:
        sys.exit("Output .sdf file already exists. Exiting.\n")
        return
    if not ofs.open(outfile):
        oechem.OEThrow.Fatal("Unable to open %s for writing" % outfile)

    ### Loop over mols.
    for f in molfiles:
        print(f)

        ifs = oechem.oemolistream()
        if not ifs.open(f):
             oechem.OEThrow.Warning("Unable to open %s for reading" % f)
        try:
            mol = next(ifs.GetOEMols())
        except StopIteration:
            print('No mol loaded for %s' % mol.GetTitle())
        ifs.close()
        mol.SetTitle(f.split('/')[-1].split('.')[0])
        oechem.OEWriteConstMolecule(ofs, mol)

    ofs.close()


# ------------------------- Parse Inputs ----------------------- #


if __name__ == "__main__":

    import argparse
    parser = argparse.ArgumentParser(description="Combine a set of molecule "
            "files such as pdb or mol2 into a single sdf file.")

    parser.add_argument('-i', '--infiles',
            help = "Path to directory containing all molecule files.")

    parser.add_argument('-t', '--ftype',
            help = "Name of the file extension. Ex: pdb or mol2")

    parser.add_argument('-o', '--outfile',
            help = "Name of output SDF file with all mols in input directory.")

    args = parser.parse_args()
    combineSDF(args.infiles, args.ftype, args.outfile)

