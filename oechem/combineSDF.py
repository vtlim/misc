#!/usr/bin/env python

# By: Victoria T. Lim

import os, sys, glob
import openeye.oechem as oechem


# --------------------------- Main Function ------------------------- #

def combineSDF(infiles, outfile):
    molfiles = glob.glob(os.path.join(infiles, '*.pdb'))

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
            print('No mol loaded for %s (StopIteration exception)' % mol.GetTitle())
        ifs.close()
        mol.SetTitle(f.split('/')[-1].split('.')[0])
        oechem.OEWriteConstMolecule(ofs, mol)

    ofs.close()


# ------------------------- Parse Inputs ----------------------- #



if __name__ == '__main__':
    from optparse import OptionParser

    parser = OptionParser(usage = "Combine a set of molecule files such as pdb\
 or mol2 into a single sdf file for use with other scripts. ")

    parser.add_option('-i', '--infiles',
            help = "Path to directory containing all molecule files.\
 Change the extension in this script if necessary.",
            type = "string",
            dest = 'infiles')

    parser.add_option('-o', '--outfile',
            help = "Name of output SDF file with all mols in input directory.",
            type = "string",
            dest = 'outfile')

    (opt, args) = parser.parse_args()
    combineSDF(opt.infiles, opt.outfile)

