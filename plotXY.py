#!/usr/bin/python

# Generate XY line plots from text data file.
#   Options include plotting specific columns, separating data to subplots,
#   subsampling data, taking running mean over data, and plotting alongside
#   uncertainty values from another data file.
#
# If combining data together from multiple files, Google Sheets can help.
#   Then copy from sheets into vim window.
#   Then replace variable number of spaces with this cmd :%s/ \{2,}/ /g
#
# By: Victoria T. Lim
#
# TODO:
#  - Write documentation
#  - Plot specific columns only

import os
import sys
import numpy as np
from pymbar import timeseries
from functools import reduce
import matplotlib.pyplot as plt
import matplotlib as mpl

# ===========================================



def subSample(x, y_mat, num_cols):
    """
    Parameters
    ----------
    x
    y_mat
    num_cols

    Returns
    -------

    """
    x_mat = []
    z_mat = [] # subsampled y_mat
    for i in range(num_cols):
        y = y_mat[:,i]
        # Compute correlation times.
        g = timeseries.statisticalInefficiency(y)
        indices = timeseries.subsampleCorrelatedData(y, g)
        # Subsample data.
        y_sub = y[indices]
        x_sub = x[indices]
        z_mat.append(y_sub)
        x_mat.append(x_sub)
        print("\nLength of original timeseries data: %d\nLength of subsampled\
 timeseries data: %d" % (len(y), len(y_sub)) )
    return x_mat, z_mat


def runningMean(y_mat, N, num_cols):
    """
    Parameters
    ----------
    y_mat
    N
    num_cols

    Returns
    -------

    Reference
    ---------
    http://stackoverflow.com/questions/13728392/moving-average-or-running-mean
    """

    z_mat = [] # subsampled y_mat
    for i in range(num_cols):
        try:
            y = y_mat[:,i] # normal data in np array(s)
        except TypeError:  # data grouped as list of np arrays
            y = y_mat[i]
        y_mean = np.convolve(y, np.ones((N,))/N,mode='valid')
        z_mat.append(y_mean)
    return z_mat

def factorize(n):
    """
    Reference
    ---------
    https://tinyurl.com/ybmgaqdt

    """
    return sorted(set(reduce(list.__add__,
           ([i, n//i] for i in range(1, int(pow(n, 0.5) + 1)) if n % i == 0))))

def formatFig(ax1, plt, **kwargs):
    """
    """

    if opt['legend'] is not None:
        leglabel = opt['legend'].split(';')
        legend=True
    if opt['group'] != 0:
        print("VTL add legend details for grouped data")
        print("VTL add legend details for grouped data")
        tSize = 12
        xSize = 8
        ySize = 8
        kSize = 8
    elif opt['publish']:
        tSize = 12
        xSize = 8
        ySize = 8
        kSize = 8
        fig.set_size_inches(3.37,1.7)
        if 'legend' in locals():
            leg = ax1.legend(leglabel,loc='upper center',fontsize=8,bbox_to_anchor=(0.50,1.30),ncol=2)
    else:
        tSize = 20
        xSize = 18
        ySize = 18
        kSize = 16
        if 'legend' in locals():
            leg = ax1.legend(leglabel,loc='upper left')

    ### Label the figure.
    ax1.set_title(opt['title'],fontsize=tSize)
    ax1.set_xlabel(opt['xlabel'],fontsize=xSize)
    ax1.set_ylabel(opt['ylabel'],fontsize=ySize)
    for xtick in ax1.get_xticklabels():
        xtick.set_fontsize(kSize)
    for ytick in ax1.get_yticklabels():
        ytick.set_fontsize(kSize)



def xyPlot(**kwargs):
    """
    """

    ### Assign input arguments.
    filename = opt['input']
    uncertf = opt['uncert']
    doSubsample =  opt['subsample']
    num_groups = opt['group']

    if opt['mean'] != 0:
        runMean = True
        runLength = int(opt['mean'])
    if opt['columns'] is not None:
        cols = list(map(int,opt['columns'].split(';')))

    ### Read in data.
    data = np.loadtxt(filename)
    if uncertf is not None:
        uncerts = np.loadtxt(uncertf)
    x = data[:,0]
    y_mat = data[:,1:]
    num_cols = y_mat.shape[1]
    if num_cols == 1: y_mat = y_mat.flatten()
    if num_groups != 0:
        if num_cols != 1:
            sys.exit("ERROR: This script is not equipped to break input "
                     "data into groups with multiple data columns.")
        if doSubsample:
            sys.exit("ERROR: This script is not yet equipped to subsample "
                     "along with breaking data into groups.")
        y_mat = np.array_split(y_mat, num_groups) # LIST of subarrays, may not be equally split
        num_cols = len(y_mat)
    print("How many data series to plot: {}".format(num_cols))

    ### subsample data (may not want to if not timeseries data!)
    if doSubsample:
        x_mat, y_mat = subSample(x,y_mat,num_cols)
    elif 'runMean' in locals():
        y_mat = runningMean(y_mat,runLength,num_cols)
        # x may not directly match with y bc of running mean
        x = 0.002*np.asarray(range(len(y_mat[0])),dtype=np.float32)


    ### Initialize figure.
    colors = mpl.cm.tab20(np.linspace(0, 1, num_cols)) # colors for plot
    num_plots = 1
    if num_groups != 0:
        factors = factorize(num_groups)
        num_plots = int(input("\nInput with {} data points will be separated into {} "
              "groups for plotting.\nDo you want to separate these groups into "
              "separate subplots?\nType 0 for no, or type an integer for "
              "the number of subplots desired.\nTo evenly distribute the lines, "
              "use one of {}. ".format(len(x),num_groups,factors)))
        lines_per_plot = int(num_groups/num_plots)

    fig, axs = plt.subplots(1, num_plots, sharey=True)
    if num_plots == 1:
        curr_ax = axs
    else:
        idx = 0
        curr_ax = axs[idx]

    ### Plot the data.
    for i in range(num_cols):
        if num_groups != 0: # most specific case
            y = y_mat[i]
            x = np.arange(len(y))
            if (num_plots != 0) and (i>0) and (i%lines_per_plot == 0):
                idx += 1
                print("Switching to new subplot...")
                formatFig(curr_ax,plt,**opt)
                curr_ax = axs[idx]
        elif doSubsample:
            x = x_mat[i]
            y = y_mat[i]
        elif 'runMean' in locals():
            y = y_mat[i]
        elif num_cols == 1:
            y = y_mat
        else:
            y = y_mat[:,i]
        print(i, len(x), y.shape)
        if uncertf is not None: # UNTESTED as of 4/6/18
            curr_ax.errorbar(x,y,yerr=u_mat[i],capsize=0.8,lw=0.8,color=color[i])
        else:
            curr_ax.plot(x, y, lw=0.8, color=colors[i]) # thinner line

    ### Format figure.
#    axes = plt.gca()
#    axes.set_xlim([min(x)-2,max(x)+2])
#    axes.set_ylim([-0.1,3])
#    ax1.text(2,11,"A",fontsize=10) # custom text on plot
    if num_groups != 0:
        plt.subplots_adjust(wspace=0.)
    formatFig(curr_ax,plt,**opt)

    ### Save figure.
    if opt['publish']:
        plt.savefig(opt['output'], bbox_inches='tight',dpi=300)
    else:
        plt.savefig(opt['output'], bbox_inches='tight')
    plt.show()


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()

    # DATA INPUT
    parser.add_argument("-i", "--input",
                        help="Name of the input file. First line is assumed "
                        "to be some heading line and is NOT read in.")
    parser.add_argument("-u", "--uncert",default=None,
                        help="Name of the file with corresponding uncertainties"
                        + ". Not compatible with running means or subsampling.")
    parser.add_argument("-c", "--columns",default=None,
                        help="Specify particular data columns to plot. Separate"
                        " values with semicolon. 0th column is x, so don't specify"
                        " 0. If not specified, will only plot first data column."
                        "TODO")
    parser.add_argument("-g", "--group", default=0, type=int,
                        help="If specified, break the data up into this many "
                        " groups to plot separately. E.g., a datafile might"
                        " be 100 lines long but you may want to plot 5 lines of"
                        " 20. Then use an argument of 5.")

    # DATA PROCESSING
    parser.add_argument("-m", "--mean", default=0,
                        help="If not default=0, take running means over the "
                        + "specified number of data points for each column.")
    parser.add_argument("-s", "--subsample", action="store_true",default=False,
                        help="Subsample y data based on correlation times.")

    # PLOT LABELING AND FORMATTING
    parser.add_argument("-x", "--xlabel",default="",
                        help="Label for x data.")
    parser.add_argument("-y", "--ylabel",default="",
                        help="Label for y data.")
    parser.add_argument("-t", "--title",default="",
                        help="Label for plot title.")
    parser.add_argument("-l", "--legend",default=None,
                        help="Add legend to data. Format input as data1;data2;...")
    parser.add_argument("-o", "--output",
                        help="Name of the output figure.")
    parser.add_argument("--publish", action="store_true",default=False,
                        help="Reduce figure/font sizes for publications.")

    args = parser.parse_args()
    opt = vars(args)
    xyPlot(**opt)
