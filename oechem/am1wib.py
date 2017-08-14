
# By: Victoria T. Lim

import argparse
import math
import os, sys
import openeye.oechem as oechem
import openeye.oequacpac as oequacpac


def am1wib(insdf):
    """
    Parameters
    ----------
    insdf: string, name of SDF file

    """
    ### Read in .sdf file and distinguish each molecule's conformers
    ifs = oechem.oemolistream()
    ifs.SetConfTest( oechem.OEAbsoluteConfTest() )
    if not ifs.open(insdf):
        oechem.OEThrow.Warning("Unable to open %s for reading" % insdf)
        return

    for mol in ifs.GetOEMols():
        print('\n\nMolecule: %s\tNumConfs: %d' % (mol.GetTitle(), mol.NumConfs()))
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
                nbors = list(atom.GetAtoms())
                ang1 = math.degrees(oechem.OEGetAngle(conf, nbors[0],atom,nbors[1]))
                ang2 = math.degrees(oechem.OEGetAngle(conf, nbors[1],atom,nbors[2]))
                ang3 = math.degrees(oechem.OEGetAngle(conf, nbors[2],atom,nbors[0]))
                print("\nSum of angles around N of index %d: %f" % (atom.GetIdx(),math.fsum([ang1,ang2,ang3])))
                for bond in atom.GetBonds():
                    nbor = bond.GetNbr(atom)
                    print ("Wiberg bond order to index ",nbor.GetIdx(), end=" ")
                    print(bond.GetData('WibergBondOrder'))



    ifs.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    req = parser.add_argument_group('required arguments')

    req.add_argument("-f", "--filename",
        help="SDF file to be processed.")
    args = parser.parse_args()
    opt = vars(args)
    if opt['filename'] is None:
        print("ERROR: no input file specified.")
        exit()

    am1wib(opt['filename'])
