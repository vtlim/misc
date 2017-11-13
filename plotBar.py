
# By: Victoria T. Lim

import os
import openeye.oechem as oechem
import numpy as np
import argparse

import matplotlib.pyplot as plt


### ------------------- Script -------------------

def plotBar(opt):
    """
    Parameters
    ----------
    opt: dictionary from parser with keys for input, XY labels, figname
    """
    infile = opt['infile']
    xlabel = opt['xlabel']
    ylabel = opt['ylabel']
    figname = opt['output']

    with open(infile,'r') as f:
        zipdata = zip(*[line.split() for line in f])
        listdata = [list(a) for a in zipdata]
        xlist = [float(i) for i in listdata[0]]
        ylist = [float(i) for i in listdata[1]]

    fig = plt.figure()
    plt.ylabel(ylabel,fontsize=14)
    plt.xlabel(xlabel,fontsize=14)
    plt.bar(xlist, ylist,align='center',ecolor='k')
#    plt.ylim(-1, 16)
#    plt.xticks(range(RefNumConfs),xlabs,fontsize=12)
#    plt.yticks(fontsize=12)
#    plt.grid()


    plt.savefig(figname,bbox_inches='tight')
    plt.show()




### ------------------- Parser -------------------

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("-i", "--infile",
        help="Input file with x in 1st column, y in 2nd column."+
             "TODO add features for plot labels in 3rd column "+
             "and stdev in 4th column.")
    parser.add_argument("-x", "--xlabel",default="",
                        help="Label for x data.")
    parser.add_argument("-y", "--ylabel",default="",
                        help="Label for y data.")
    parser.add_argument("-o", "--output",
                        help="Name of the output figure.", default='barplot.eps')


    args = parser.parse_args()
    opt = vars(args)
    if not os.path.exists(opt['infile']):
        raise parser.error("Input file %s does not exist." % opt['infile'])

    plotBar(opt)
