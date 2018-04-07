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
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from pymbar import timeseries

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
        y = y_mat[:,i]
        y_mean = np.convolve(y, np.ones((N,))/N,mode='valid')
        z_mat.append(y_mean)
    return z_mat


def xyPlot(**kwargs):

    def formatFig(ax1, plt, legend):

        if publish:
            tSize = 12
            xSize = 8
            ySize = 8
            kSize = 8
            fig.set_size_inches(3.37,1.7)
            if legend:
                leg = ax1.legend(leglabel,loc='upper center',fontsize=8,bbox_to_anchor=(0.50,1.30),ncol=2)
        else:
            tSize = 20
            xSize = 18
            ySize = 18
            kSize = 16
            if legend:
                leg = ax1.legend(leglabel,loc='upper left')

        ### Label the figure.
        ax1.set_title(plttitle,fontsize=tSize)
        ax1.set_xlabel(xlabel,fontsize=xSize)
        ax1.set_ylabel(ylabel,fontsize=ySize)
        for xtick in ax1.get_xticklabels():
            xtick.set_fontsize(kSize)
        for ytick in ax1.get_yticklabels():
            ytick.set_fontsize(kSize)

        ### Save figure.
        if publish:
            plt.savefig(figname, bbox_inches='tight',dpi=300)
        else:
            plt.savefig(figname, bbox_inches='tight')

        plt.show()

    filename = opt['input']
    uncertf = opt['uncert']
    doSubsample =  opt['subsample']
    xlabel = opt['xlabel']
    ylabel = opt['ylabel']
    plttitle = opt['title']
    legend = opt['legend']
    figname = opt['output']
    publish =  opt['publish']

    if opt['mean'] != 0:
        runMean = True
        runLength = int(opt['mean'])
    else:
        runMean = False
    if opt['columns'] is not None:
        cols = list(map(int,opt['columns'].split(',')))
    if opt['legend'] is not None:
        leglabel = opt['legend'].split(';')
        legend=True

    ### Read in data.
    data = np.loadtxt(filename)
    if uncertf is not None:
        uncerts = np.loadtxt(uncertf)
    x = data[:,0]
    y_mat = data[:,1:]
    try:
        num_cols = y_mat.shape[1]
    except IndexError:
        num_cols = 1
    if num_cols == 1: y_mat = y_mat.flatten()
    print("Number of data columns parsed: {}".format(num_cols))

    ### subsample data (may not want to if not timeseries data!)
    if doSubsample: x_mat, y_mat = subSample(x,y_mat,num_cols)
    if runMean:
        y_mat = runningMean(y_mat,runLength,num_cols)
        # x may not directly match with y bc of running mean
        x = 0.002*np.asarray(range(len(y_mat[0])),dtype=np.float32)

    ### Initialize figure and set plot limits.
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    axes = plt.gca()
    axes.set_xlim([min(x)-0.2,max(x)+0.2])
#    axes.set_ylim([-0.1,3])

    ### Color the rainbow.
    colors = mpl.cm.tab20(np.linspace(0, 1, num_cols))

    ### Plot the data.
    for i in range(num_cols):
        if doSubsample:
            x = x_mat[i]
            y = y_mat[i]
        elif runMean:
            y = y_mat[i]
        elif num_cols == 1:
            y = y_mat
        else:
            y = y_mat[:,i]
        print(len(x),y.shape)
        if uncertf is not None:
            # UNTESTED as of 4/6/18
            ax1.errorbar(x,y,yerr=u_mat[i],capsize=0.8,lw=0.8,color=color[i])
        else:
            ax1.plot(x, y, lw=0.8, color=colors[i]) # thinner line

    ### Custom text on plot
#    ax1.text(2,11,"A",fontsize=10)

    formatFig(ax1,plt,legend)


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
                        " values with commas. 0th column is x, so don't specify"
                        " 0. If not specified, will only plot first data column."
                        "TODO")
    parser.add_argument("-c", "--columns",default=None,
                        help="Specify particular data columns to plot. Separate"
                        " values with commas. 0th column is x, so don't specify"
                        " 0. If not specified, will only plot first data column."
                        "TODO")

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
