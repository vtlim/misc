
# By: Victoria T. Lim

import os
import openeye.oechem as oechem
import numpy as np
import argparse
import collections

import matplotlib as mpl
import matplotlib.pyplot as plt


### ------------------- Script -------------------

def extractXY(fname, tag):

    ifs = oechem.oemolistream()
    ifs.SetConfTest( oechem.OEAbsoluteConfTest() )
    if not ifs.open(fname):
        oechem.OEThrow.Warning("Unable to open %s for reading" % fname)

    xlist = []
    ylist = []

    for mol in ifs.GetOEMols():
        for j, conf in enumerate( mol.GetConfs() ):
            xlist.append(int(mol.GetTitle()))
            ylist.append(float(oechem.OEGetSDData(conf, tag)))

    ### convert to numpy array, take relative e, convert to kcal/mol
    ylist = np.array(ylist)
    ylist = ylist - ylist[0]
    ylist = 627.5095*ylist
    return xlist, ylist


def plotMultSDF(wholedict, figname,verbose):
    """
    Parameters
    ----------
    """
    numFiles = len(wholedict)
    xarray = []
    yarray = []
    labels = []
    for i in wholedict:
        print(wholedict[i]['fname'], wholedict[i]['label'])
        xdata, ydata = extractXY(wholedict[i]['fname'], wholedict[i]['tag'])
        labels.append(wholedict[i]['label'])
        xarray.append(xdata)
        yarray.append(ydata)

    if verbose:
        with open('results.dat','w') as f:
            for l in labels:
                f.write("# %s\n" % l)
            tmpray = list(yarray) # make a copy and not a pointer
            tmpray.insert(0,xdata)
            for y in zip(*tmpray):
                f.write("{0}\t{1}\t{2}\t{3}\t{4}\n".format(*y))


    fig = plt.figure()
    xlabel='OCOH dihedral angle (deg)'
    ylabel="rel. energy (kcal/mol)"

    colors = mpl.cm.rainbow(np.linspace(0, 1, numFiles))
    #for i in reversed(range(numFiles)):
    for i, (xs, ys) in enumerate(zip(xarray,yarray)):
        plt.plot(xs,ys,lw=0.8,color=colors[i],label=labels[i])

    xvtl = [0,180]
    yvtl = [0.,-0.4727]
    plt.scatter(xvtl, yvtl, s=5.5,color='black', label='explicit waters')


    plt.ylim(-2.0,16)
    plt.grid()

    # publication view
    plt.ylabel(ylabel,fontsize=8)
    plt.xlabel(xlabel,fontsize=8)
    plt.legend(bbox_to_anchor=(0.08,1.05),loc=3,fontsize=8)
    fig.set_size_inches(3.37,1.7)
    plt.savefig(figname,bbox_inches='tight',dpi=300)

    # standard view
#    plt.ylabel(ylabel,fontsize=14)
#    plt.xlabel(xlabel,fontsize=14)
#    plt.legend(bbox_to_anchor=(1.05, 1), loc=2)
#    plt.savefig(figname,bbox_inches='tight')


    plt.show()





### ------------------- Parser -------------------

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("-i", "--infile",
        help="Input file with each line containing file info to be plotted.\
 Format each line as [filename] ['SD tag'] with no square brackets\
 but SD tags do need single quotes.")

    parser.add_argument("-o", "--outplot",default='lineplot.png',
        help="")
    parser.add_argument("-v", "--verbose",action="store_true",default=False,
        help="")

    args = parser.parse_args()
    opt = vars(args)
    if not os.path.exists(opt['infile']):
        raise parser.error("Input file %s does not exist." % opt['infile'])



    # Read input file and store each file's information in an overarching set.
    # http://stackoverflow.com/questions/25924244/creating-2d-dictionary-in-python
    linecount = 0
    wholedict = collections.OrderedDict()
    with open(opt['infile']) as f:
        for line in f:
            if line.startswith('#'):
                continue
            dataline = [x.strip() for x in line.split('\'')]
            wholedict[linecount] = {'fname':dataline[0],'tag':dataline[1],'label':dataline[3]}
            linecount += 1

    plotMultSDF(wholedict,opt['outplot'],opt['verbose'])
