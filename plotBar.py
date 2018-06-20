
# By: Victoria T. Lim

import os
import numpy as np
import argparse
import matplotlib.pyplot as plt


### ------------------- Script -------------------

def parse_file(infile):
    """


    Parameters
    ----------

    """

    with open(infile,'r') as f:
        zipdata = zip(*[line.split(';') for line in f if not line.startswith(("#","\n"))])
        listdata = [list(a) for a in zipdata]
        xlist = [float(i) for i in listdata[0]]
        ylist = [float(i) for i in listdata[1]]
        try:
            llist = [i.strip() for i in listdata[2]]
        except IndexError:
            llist = []

    return xlist, ylist, llist

def plot_bar_group(xlist, ylist, xlabel='', ylabel='', horiz=False):
    """
    Generating the bar plot in small groups at a time gives the members
        of a given group different colors.
    For the same input of `plot_bar` and `plot_bar_group`, the output plots are
        mostly the same with the only differences of figure size (if specified)
        and the colors.


    Parameters
    ----------

    """

    refx = -5000
    grpX = [[]] # list of lists for grouped bar plot
    grpY = [[]]
    for x, y in zip(xlist,ylist):
        # new group if x value is 2+ integers apart
        if abs(x-refx)>1:
            idx = 0
            refx = x
        # if x is adjacent (1 space apart) then same group
        elif abs(x-refx)==1:
            idx+=1
            refx = x
        # add data into previously defined group
        try:
            grpX[idx].append(x)
            grpY[idx].append(y)
        # define new group (sublist) and add data
        except IndexError as e:
            grpX.append([])
            grpY.append([])
            grpX[idx].append(x)
            grpY[idx].append(y)

    fig = plt.figure(figsize=(18,8))
    plt.ylabel(ylabel,fontsize=18)
    plt.xlabel(xlabel,fontsize=18)

    for xlist, ylist in zip(grpX, grpY):
        if horiz:
            plt.barh(xlist,ylist,align='center',height=1.0,edgecolor='white',ecolor='k')
        else:
            plt.bar(xlist,ylist,align='center',width=1.0,edgecolor='white',ecolor='k',zorder=3)

    return plt

def plot_bar(xlist, ylist, xlabel='', ylabel='', horiz=False):
    """


    Parameters
    ----------

    """
    fig = plt.figure()
    plt.ylabel(ylabel,fontsize=16)
    plt.xlabel(xlabel,fontsize=16)
    if horiz:
        plt.barh(xlist,ylist,align='center',edgecolor='white',ecolor='k',zorder=3)
    else:
        plt.bar(xlist,ylist,align='center',width=1.0,edgecolor='white',ecolor='k',zorder=3)
    return plt


def plot_line(xlist, ylist, xlabel='', ylabel='', horiz=False):
    """


    Parameters
    ----------

    """
    fig = plt.figure()
    plt.ylabel(ylabel,fontsize=16)
    plt.xlabel(xlabel,fontsize=16)

    # define colors, either a single one, or a list
    cs = ['orange','g','b','m','b','b']
    #cs = 'k'

    if horiz:
        print("not supported yet (TODO)")
    else:
        plt.vlines(xlist, np.zeros(len(xlist)), ylist, cs, linestyles='dashed')
        plt.scatter(xlist, ylist, c=cs)
    return plt


def finalize_and_save(plt, xlist, ylist, llist, figname):
    """
    Customize plot with grid, labels, and/or other features.
    Then save and show figure.

    Parameters
    ----------

    """

    # use labels on the x ticks
    if len(llist) == len(xlist):
        plt.xticks(xlist, llist, rotation=-40, horizontalalignment='left') # default align is center

#    # use labels on the y ticks -- if horiz, use xlist
#    if len(llist) == len(xlist):
#        plt.yticks(xlist, llist)

#    plt.ylim(330, 362)
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)

    # ===== GRID AND TICK OPTIONS ===== #
#    plt.grid()

#    plt.gca().xaxis.grid(True)  # only show vertical grid
#    plt.tick_params(
#        axis='y',          # change settings for y-axis
#        which='both',      # change settings for both major and minor ticks
#        left='off')        # turn off ticks along the bottom edge

#    # show horizontal grid and don't show xticks or xticklabels
    plt.gca().yaxis.grid(True)  # only show horizontal grid
#    plt.tick_params(
#        axis='x',          # change settings for x-axis
#        which='both',      # change settings for both major and minor ticks
#        bottom='off',      # turn off ticks along the bottom edge
#        top='off',         # turn off ticks along the top edge
#        labelbottom='off') # turn off tick labels along the bottom edge

    plt.savefig(figname,bbox_inches='tight')
    plt.show()




### ------------------- Parser -------------------

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    # input data
    parser.add_argument("-i", "--infile",
        help="Input file with x in 1st column, y in 2nd column."+
             "TODO add features for plot labels in 3rd column "+
             "and stdev in 4th column.")

    # plot labeling
    parser.add_argument("-x", "--xlabel",default="",
        help="Label for x data. Use single quotes if passing in Latex.")
    parser.add_argument("-y", "--ylabel",default="",
        help="Label for y data. Use single quotes if passing in Latex.")
    parser.add_argument("-o", "--output",
        help="Name of the output figure.", default='barplot.png')

    # plot type
    parser.add_argument("--group",action="store_true",default=False,
        help="Cluster bars by x-index. Consecutive x's are in "+
        "same group. Non-consecutive x's are in separate groups. "+
        "E.g., the cluster for x=1,2,3 is separated from x=5,6")
    parser.add_argument("--line",action="store_true",default=False,
        help="Generate line plots in the style of bar plots.")
    parser.add_argument("--horiz",action="store_true",default=False,
        help="Generate bar plot with horizontal bars. Default is vertical.")


    args = parser.parse_args()
    opt = vars(args)
    if not os.path.exists(opt['infile']):
        raise parser.error("Input file %s does not exist." % opt['infile'])

    xlist, ylist, llist = parse_file(opt['infile'])
    if opt['group']:
        plt = plot_bar_group(xlist, ylist, opt['xlabel'], opt['ylabel'], opt['horiz'])
    elif opt['line']:
        plt = plot_line(xlist, ylist, opt['xlabel'], opt['ylabel'], opt['horiz'])
    else:
        plt = plot_bar(xlist, ylist, opt['xlabel'], opt['ylabel'], opt['horiz'])
    finalize_and_save(plt, xlist, ylist, llist, opt['output'])

