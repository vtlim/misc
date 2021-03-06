
# By: Victoria T. Lim

import os
import numpy as np
import argparse
import matplotlib.pyplot as plt


### ------------------- Script -------------------

def parse_file(infile):
    """
    Parse the input file. Columns must be separated by semicolons, and ordered
      as follows: (1) x-value, (2) y-value, (3) label, (4) error bar.
    If you have error bars but don't want labels, just fill in some text placeholder.

    Parameters
    ----------
    infile : string
        Name of the input file

    """

    with open(infile,'r') as f:
        zipdata = zip(*[line.split(';') for line in f if not line.lstrip(' ').startswith(("#","\n"))])
        listdata = [list(a) for a in zipdata]
        xlist = [float(i) for i in listdata[0]]
        ylist = [float(i) for i in listdata[1]]
        try:
            llist = [i.strip() for i in listdata[2]]
        except IndexError:
            llist = []
        try:
            elist = [float(i) for i in listdata[3]]
        except IndexError:
            elist = np.zeros(len(xlist))

    return xlist, ylist, llist, elist


def initiate_plot(xlabel, ylabel, publish):
    """
    publish : Bool
        Format figure for article publication.
    """
    if publish:
        fig = plt.figure()
        #fig.set_size_inches(3.37,1.7)
        fig.set_size_inches(6.5,3.0)
        plt.ylabel(ylabel,fontsize=10)
        plt.xlabel(xlabel,fontsize=10)
        plt.xticks(fontsize=10)
        plt.yticks(fontsize=10)
        return fig, plt

    fig = plt.figure(figsize=(12,8))
    plt.ylabel(ylabel,fontsize=16)
    plt.xlabel(xlabel,fontsize=16)
    plt.xticks(fontsize=16)
    plt.yticks(fontsize=16)

    return fig, plt


def plot_bar_group(plt, xlist, ylist, elist, horiz=False):
    """
    Generate the bar plot in small groups at a time. Each bar of a group
        has a different color (e.g., blue yellow green in a group).
    If same input is fed to `plot_bar` and `plot_bar_group`, the output plots are
        mostly same with the only differences of figure size (if specified)
        and the colors.


    Parameters
    ----------
    xlist
    ylist
    horiz

    """
    #colors = ['purple','lightseagreen']
    legends = ['ZPVE-CCSD(T)/CBS limit','CCSD(T)/CBS limit','MP2/CBS limit','B3LYP-D3/cc-pVTZ','TPSSh-D3BJ/def2-TZVP','COSMO-B3LYP-D3/cc-pVTZ','COSMO-B3LYP-D3/cc-pVTZ']
    legends = ['2GBI taut1', '2GBI taut2', 'expt']


    refx = -5000  # some start int for ref group
    count = 0     # define for elist in case empty
    grpX = [[]]   # list of lists for grouped bar plot
    grpY = [[]]
    grpE = [[]]
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
            if len(elist) != 0:
                grpE[idx].append(elist[count])
        # define new group (sublist) and add data
        except IndexError as e:
            grpX.append([])
            grpY.append([])
            grpX[idx].append(x)
            grpY[idx].append(y)
            if len(elist) != 0:
                grpE.append([])
                grpE[idx].append(elist[count])

        count += 1

    plot_settings = {'zorder':3, 'alpha':0.9, 'align':'center', 'edgecolor':'white', 'ecolor':'k'}
    error_config = {'zorder':5}

    for i, (xlist, ylist) in enumerate(zip(grpX, grpY)):
        # determine if there is an error list, if not grpE is len 1
        if len(grpE) != 1:
            errs = grpE[i]
        else:
            errs = np.zeros(len(xlist))

        # do the plotting
        if horiz:
            bars = plt.barh(xlist,ylist,xerr=errs,height=1.0,**plot_settings)
        else:
            # zorder controls layering; higher zorder is more on top
            bars = plt.bar(xlist,ylist,yerr=errs,width=1.0,error_kw=error_config,**plot_settings)

        # see if custom colors were defined
        try:
            [b.set_facecolor(colors[i]) for b in bars]
        except NameError:
            pass

        # see if custom legend was input, but only do this once
        try:
            bars[0].set_label(legends[i])
        except NameError:
            pass

    return plt

def plot_bar(plt, xlist, ylist, elist, horiz=False):
    """


    Parameters
    ----------

    """

    plot_settings = {'zorder':3, 'alpha':0.9, 'align':'center', 'edgecolor':'white', 'ecolor':'k'}
    error_config = {'zorder':5}

    if horiz:
        plt.barh(xlist,ylist,xerr=elist,height=1.0,**plot_settings)
    else:
        plt.bar(xlist,ylist,yerr=elist,width=1.0,**plot_settings)
    return plt


def plot_line(plt, xlist, ylist, horiz=False):
    """


    Parameters
    ----------

    """

    # define colors, either a single one, or a list
    cs = ['orange','g','b','m','b','b']
    #cs = 'k'

    if horiz:
        print("not supported yet (TODO)")
    else:
        plt.vlines(xlist, np.zeros(len(xlist)), ylist, cs, linestyles='dashed')
        plt.scatter(xlist, ylist, c=cs)
    return plt


def finalize_and_save(plt, xlist, ylist, llist, figname, horiz):
    """
    Customize plot with grid, labels, and/or other features.
    Then save and show figure.

    Parameters
    ----------

    """

#    plt.ylim(0, 7)

    # ===== CUSTOM LINE ===== #
    # include this threshold value as comment in input file for your record
    #plt.axhline(y=3.049, c='b', lw=2.0,ls='--',label='arg reference')
    #plt.axhline(y=5.012,c='r',lw=2.0,ls=':', label='ser reference')

    # ===== LEGEND OPTIONS ===== #
    plt.legend(loc=2,fontsize=8)
    #plt.legend(loc='center left', bbox_to_anchor=(1, 0.5), fontsize=8)

    # ====== TICK LABEL OPTIONS ======= #
    if horiz:
        # use labels on the y ticks (but still want xlist)
        if len(llist) == len(xlist):
            plt.yticks(xlist, llist)
    else:
        # use labels on the x ticks
        if len(llist) == len(xlist):
            plt.xticks(xlist, llist, rotation=-40, horizontalalignment='left') # default align is center

    # ===== GRID AND TICK OPTIONS ===== #
#    plt.grid()

#    # show horizontal grid and don't show xticks or xticklabels
#    plt.gca().yaxis.grid(True)  # only show horizontal grid
#    plt.tick_params(
#        axis='x',          # change settings for x-axis
#        which='both',      # change settings for both major and minor ticks
#        bottom='off',      # turn off ticks along the bottom edge
#        top='off',         # turn off ticks along the top edge
#        labelbottom='off') # turn off tick labels along the bottom edge

    plt.gca().xaxis.grid(True)  # only show vertical grid
    plt.tick_params(
        axis='y',          # change settings for y-axis
        which='both',      # change settings for both major and minor ticks
        left='off')        # turn off ticks along the bottom edge


    # ===== FINALIZE AND SAVE ========= #
#    plt.title('taut1')
#    plt.ylim(0, 9.2)

    plt.savefig(figname,bbox_inches='tight')
    plt.show()




### ------------------- Parser -------------------

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    # input data
    parser.add_argument("-i", "--infile",
        help="Input file with x in 1st column, y in 2nd column."+
             "Optional: plot labels in 3rd column, stdev in 4th column.")

    # plot labeling
    parser.add_argument("-o", "--output",
        help="Name of the output figure.", default='barplot.png')
    parser.add_argument("-x", "--xlabel",default="",
        help="Label for x data. Use single quotes if passing in Latex.")
    parser.add_argument("-y", "--ylabel",default="",
        help="Label for y data. Use single quotes if passing in Latex.")

    # plot type
    parser.add_argument("--group",action="store_true",default=False,
        help="Cluster bars by x-index. Consecutive x's are in "+
        "same group. Non-consecutive x's are in separate groups. "+
        "E.g., the cluster for x=1,2,3 is separated from x=5,6")
    parser.add_argument("--line",action="store_true",default=False,
        help="Generate line plots in the style of bar plots.")
    parser.add_argument("--horiz",action="store_true",default=False,
        help="Generate bar plot with horizontal bars. Default is vertical.")
    parser.add_argument("--publish",action="store_true",default=False,
        help="Format for publishing in article.")


    args = parser.parse_args()
    opt = vars(args)
    if not os.path.exists(opt['infile']):
        raise parser.error("Input file %s does not exist." % opt['infile'])

    xlist, ylist, llist, elist = parse_file(opt['infile'])
    fig, plt = initiate_plot(opt['xlabel'], opt['ylabel'], opt['publish'])
    if opt['group']:
        plt = plot_bar_group(plt, xlist, ylist, elist, opt['horiz'])
    elif opt['line']:
        plt = plot_line(plt, xlist, ylist, opt['horiz'])
    else:
        plt = plot_bar(plt, xlist, ylist, elist, opt['horiz'])
    finalize_and_save(plt, xlist, ylist, llist, opt['output'], opt['horiz'])

