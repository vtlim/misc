
# By: Victoria T. Lim

import os
import openeye.oechem as oechem
import numpy as np
import argparse

import matplotlib.pyplot as plt


### ------------------- Script -------------------

def plotSDF(infile, tag,figname='lineplot.png'):
    """
    Parameters
    ----------
    """

    ### Read in .sdf file and distinguish each molecule's conformers
    ifs = oechem.oemolistream()
    ifs.SetConfTest( oechem.OEAbsoluteConfTest() )
    if not ifs.open(infile):
        oechem.OEThrow.Warning("Unable to open %s for reading" % infile)
        return

    xlist = []
    ylist = []

    for mol in ifs.GetOEMols():
        print(mol.GetTitle(), mol.NumConfs())
        for j, conf in enumerate( mol.GetConfs() ):
            try:
                ylist.append(float(oechem.OEGetSDData(conf, tag)))
                xlist.append(int(mol.GetTitle()))
            except ValueError as err:
                pass  # mols not converged may not have tag

    ### convert to numpy array, take relative e, convert to kcal/mol
    ylist = np.array(ylist)
    ylist = ylist - ylist[0]
    ylist = 627.5095*ylist

    ### Plot.
    xlabel='conformation number'
    ylabel="Relative energy (kcal/mol)"

    fig = plt.figure()
#    ax = fig.gca()
#    ax.set_xticks(np.arange(-1,RefNumConfs+1,2))

    plt.ylabel(ylabel,fontsize=14)
    plt.xlabel(xlabel,fontsize=14)
    plt.scatter(xlist, ylist)
#    plt.plot(xlist, ylist)
    plt.ylim(-1, 16)
#    plt.xticks(range(RefNumConfs),xlabs,fontsize=12)
#    plt.yticks(fontsize=12)
    plt.grid()


    plt.savefig(figname,bbox_inches='tight')
    plt.show()




### ------------------- Parser -------------------

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("-i", "--infile",
        help="Input SDF file with all molecules and conformers.")

    parser.add_argument("-t", "--tag",
        help="SDF tag with data to be plotted.")

    args = parser.parse_args()
    opt = vars(args)
    if not os.path.exists(opt['infile']):
        raise parser.error("Input file %s does not exist." % opt['infile'])

    plotSDF(opt['infile'],opt['tag'])
