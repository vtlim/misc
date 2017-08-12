
# By: Victoria T. Lim

# Purpose: Find invertible nitrogens, and sum the angles around them for classification of geometry as planar, pyramidal, or somewhere in between.

import argparse
import math
import os, sys
import openeye.oechem as oechem


def classifyN(insdf):
    """
    Parameters
    ----------
    insdf:  string - PATH+name of SDF file
    """
    wdir = os.getcwd()

    ### Read in .sdf file and distinguish each molecule's conformers
    ifs = oechem.oemolistream()
    ifs.SetConfTest( oechem.OEAbsoluteConfTest() )
    if not ifs.open(insdf):
        oechem.OEThrow.Warning("Unable to open %s for reading" % insdf)
        return

    ### Loop over conf of each mol
    for mol in ifs.GetOEMols():
        print('\n%s\t%d' % (mol.GetTitle(), mol.NumConfs()))
        for i, conf in enumerate( mol.GetConfs()):

            for atom in conf.GetAtoms(oechem.OEIsInvertibleNitrogen()):
                nbors = list(atom.GetAtoms())
                ang1 = math.degrees(oechem.OEGetAngle(conf, nbors[0],atom,nbors[1]))
                ang2 = math.degrees(oechem.OEGetAngle(conf, nbors[1],atom,nbors[2]))
                ang3 = math.degrees(oechem.OEGetAngle(conf, nbors[2],atom,nbors[0]))
                print("Invertible N with index %d: %f" % (atom.GetIdx(),math.fsum([ang1,ang2,ang3])))
    ifs.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    req = parser.add_argument_group('required arguments')

    req.add_argument("-f", "--filename",
        help="SDF file to be processed.")
    args = parser.parse_args()
    opt = vars(args)

    classifyN(opt['filename'])
