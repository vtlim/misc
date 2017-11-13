
# By: Victoria T. Lim
# Purpose: Find invertible nitrogens, and calculate their sum of angles 
#          for classification of geometry from planar to pyramidal.
# Usage: python am1wib.py -i input.sdf -o output.dat -p barplot-angles.dat

import argparse
import math
import os, sys
import openeye.oechem as oechem
import openeye.oequacpac as oequacpac


def am1wib(insdf, outdat, plotout=None):
    """
    Parameters
    ----------
    insdf: string, name of SDF file

    """
    outf = open(outdat, 'w')
    ### Read in .sdf file and distinguish each molecule's conformers
    ifs = oechem.oemolistream()
    ifs.SetConfTest( oechem.OEAbsoluteConfTest() )
    if not ifs.open(insdf):
        oechem.OEThrow.Warning("Unable to open %s for reading" % insdf)
        return

    angList = [] # for plotting
    labelList = [] # for plotting
    for mol in ifs.GetOEMols():
        molName = mol.GetTitle()
        outf.write('\n\n>>> Molecule: %s\tNumConfs: %d' % (molName, mol.NumConfs()))
        for i, conf in enumerate( mol.GetConfs()):

            ### AM1-BCC charge calculation
            charged_copy = oechem.OEMol(mol)
            status = oequacpac.OEAssignPartialCharges(charged_copy, oequacpac.OECharges_AM1BCCSym, False, False)
            if not status:
                raise(RuntimeError("OEAssignPartialCharges returned error code %s" % status))

            ### Our copy has the charges we want but not the right conformation.
            ### Copy charges over. Also copy over Wiberg bond orders.
            partial_charges = []
            partial_bondorders = []
            for atom in charged_copy.GetAtoms():
                partial_charges.append( atom.GetPartialCharge() )
            for (idx,atom) in enumerate(mol.GetAtoms()):
                atom.SetPartialCharge( partial_charges[idx] )
            for bond in charged_copy.GetBonds():
                partial_bondorders.append( bond.GetData("WibergBondOrder"))
            for (idx, bond) in enumerate(mol.GetBonds()):
                bond.SetData("WibergBondOrder", partial_bondorders[idx])

            ### Sum angles around each invertible N, and get Wiberg bond order.
            for atom in conf.GetAtoms(oechem.OEIsInvertibleNitrogen()):
                aidx = atom.GetIdx()
                nbors = list(atom.GetAtoms())
                ang1 = math.degrees(oechem.OEGetAngle(conf, nbors[0],atom,nbors[1]))
                ang2 = math.degrees(oechem.OEGetAngle(conf, nbors[1],atom,nbors[2]))
                ang3 = math.degrees(oechem.OEGetAngle(conf, nbors[2],atom,nbors[0]))
                ang_sum = math.fsum([ang1,ang2,ang3])
                outf.write("\n\n%s: sum of angles for N, index %d: %f" % (molName, aidx, ang_sum))
                angList.append(ang_sum)
                labelList.append("{}_{}_{}".format(molName,i,aidx))

                for bond in atom.GetBonds():
                    nbor = bond.GetNbr(atom)
                    nidx = nbor.GetIdx()
                    nbor_wib = bond.GetData('WibergBondOrder')
                    outf.write("\n{}: wiberg bond order for indices {} {}: {}".format(molName, aidx, nidx, nbor_wib))

    if plotout is not None:
        with open(plotout,'w') as f:
            lis = [list(range(len(angList))), angList, labelList]
            for x in zip(*lis):
                f.write("{0}\t{1}\t{2}\n".format(*x))

    ifs.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    req = parser.add_argument_group('required arguments')

    req.add_argument("-i", "--input",
        help="Name of SDF file to be processed.")
    req.add_argument("-o", "--output",
        help="Name of text file for output.")
    req.add_argument("-p", "--plotout",
        help="Name of text file for plot-friendly output. "+
             "Each angle has label of molTitle_confIdx_atomIdx.")

    args = parser.parse_args()
    opt = vars(args)
    if opt['input'] is None:
        print("ERROR: no input file specified.")
        exit()
    if opt['output'] is None:
        print("ERROR: no output file specified.")
        exit()

    am1wib(opt['input'], opt['output'], opt['plotout'])
