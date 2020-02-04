#!/usr/bin/python

"""
plotXY.py

Generate XY line plots from text data file.
  Options include plotting specific columns, separating data to subplots,
  subsampling data, taking moving average over data, and plotting alongside
  uncertainty values from another data file.

This script can also be imported for subsampling in other scripts/plots.
  - sys.path.insert(0,'/DFS-L/DATA/mobley/limvt/analysis')
  - import plotXY
  - plotXY.moving_average(ydata, N)

Notes:
  - Subsampling with grouped data works by first separating the data into
    the specified number of groups, THEN subsampling.
  - If combining data together from multiple files, Google Sheets can help.
    Then copy from sheets into vim window.
    Then replace variable number of spaces with this cmd :%s/ \{2,}/ /g

By: Victoria T. Lim

TODO:
  - Write documentation

"""

import sys
import numpy as np
from functools import reduce
import matplotlib.pyplot as plt
import matplotlib as mpl

# ===========================================

def find_num_cols(y_mat):
    """
    For use in subsample or moving_average functions.
    """
    # list of np arrays
    if type(y_mat) is list:
        if len(y_mat[0]) > 1:
            num_cols = len(y_mat)
        else:
            num_cols = 1

    # 1D np array
    elif type(y_mat) is np.ndarray:
        if len(y_mat.shape) == 2:
            num_cols = y_mat.shape[1]
        else:
            num_cols = 1

    return num_cols


def subsample(x, y_mat, num_cols=None):
    """
    Parameters
    ----------
    x : numpy array
        1-dimensional array with x-data, such as timestep.
    y_mat : can take various forms:
        - list of numpy arrays, such as grouping 1-column data into smaller data series
        - 1D numpy array, such as subsampling 1-column data
        - multidimensional numpy array, if data has many columns
    num_cols : int (opt.)
        Number of data series for the input y_mat. Use this value to loop
        over the input data, since it can be formatted as 1- or N-dimensional
        list or numpy array. If num_cols not specified, the value will be
        extracted from input data using find_num_cols function.

    Returns
    -------
    x_mat : list
        multi-dimensional array of the same shape as z_mat
    z_mat : list
        multi-dimesional array in which z_mat[i][j] is the jth value in the ith data series.

    """
    from pymbar import timeseries

    x_mat = []
    z_mat = [] # subsampled y_mat

    if num_cols is None:
        num_cols = find_num_cols(y_mat)

    for i in range(num_cols):

        # list of np arrays
        if type(y_mat) is list and len(y_mat[0]) > 1:
            y = y_mat[i]

        # 1D np array
        elif type(y_mat) is np.ndarray and len(y_mat.shape) == 1:
            y = y_mat

        # multidimensional np array
        else:
            y = y_mat[:,i]

        # compute correlation times
        g = timeseries.statisticalInefficiency(y)
        indices = timeseries.subsampleCorrelatedData(y, g)

        # subsample data
        y_sub = y[indices]
        x_sub = x[indices]
        z_mat.append(y_sub)
        x_mat.append(x_sub)

        print("\nLength of original timeseries data: %d" % len(y) )
        print("\nLength of subsampled timeseries data: %d" % len(y_sub) )

    return x_mat, z_mat


def moving_average(y_mat, N, num_cols=None):
    """
    Parameters
    ----------
    y_mat : can take various forms:
        - list of numpy arrays, such as grouping 1-column data into smaller data series
        - 1D numpy array, such as taking moving average of 1-column data
        - multidimensional numpy array, if data has many columns
    N : int
        Bin width over to take the moving average.
    num_cols : int (opt.)
        Number of data series for the input y_mat. Use this value to loop
        over the input data, since it can be formatted as 1- or N-dimensional
        list or numpy array. If num_cols not specified, the value will be
        extracted from input data using find_num_cols function.

    Returns
    -------
    z_mat : list
        multi-dimensional array in which z_mat[i][j] is the jth value in the ith data series.

    Reference
    ---------
    http://stackoverflow.com/questions/13728392/moving-average-or-running-mean
    """

    z_mat = [] # for subsampled y_mat

    if num_cols is None:
        num_cols = find_num_cols(y_mat)

    for i in range(num_cols):

        # list of np arrays
        if type(y_mat) is list and len(y_mat[0]) > 1:
            y = y_mat[i]

        # 1D np array
        elif type(y_mat) is np.ndarray and len(y_mat.shape) == 1:
            y = y_mat

        # multidimensional np array
        else:
            y = y_mat[:,i]

        # calculate moving average
        y_mean = np.convolve(y, np.ones((N,))/N,mode='valid')
        z_mat.append(y_mean)

    if num_cols == 1:
        z_mat = z_mat[0]

    return z_mat


def factorize(n):
    """
    Reference
    ---------
    https://tinyurl.com/ybmgaqdt

    """
    return sorted(set(reduce(list.__add__,
           ([i, n//i] for i in range(1, int(pow(n, 0.5) + 1)) if n % i == 0))))


def format_fig(ax1, plt, fig, **kwargs):
    """
    """
    # plot limits
    #ax1.set_xlim([min(x)-2,max(x)+2])
    #ax1.set_ylim([3, 8])

    # custom text on plot
    #ax1.text(2,11,"A",fontsize=10)

    # shade custom regions
    ax1.axvspan(217, 222, facecolor='lightgrey', alpha=0.25)
    ax1.axvspan(246, 254, facecolor='lightgrey', alpha=0.25)
    ax1.axvspan(282, 286, facecolor='lightgrey', alpha=0.25)

    plt.grid()
    #plt.grid(which='minor', alpha=0.2)
    #plt.minorticks_on()

    if opt['legend'] is not None:
        leglabel = opt['legend'].split(';')
        legend=True

    if opt['publish']:
        tSize = 12
        xSize = 8
        ySize = 8
        kSize = 8
        fig.set_size_inches(3.37,1.7)
        if 'legend' in locals():
            leg = ax1.legend(leglabel, loc='upper center', fontsize=8,
                bbox_to_anchor=(0.50,1.40), ncol=2)
    else:
        tSize = 20
        xSize = 18
        ySize = 18
        kSize = 16
        fig.set_size_inches(30, 10)
        if 'legend' in locals():
            leg = ax1.legend(leglabel, loc='upper right')

    ### Label the figure.
    ax1.set_title(opt['title'],   fontsize=tSize)
    ax1.set_xlabel(opt['xlabel'], fontsize=xSize)
    ax1.set_ylabel(opt['ylabel'], fontsize=ySize)
    for xtick in ax1.get_xticklabels():
        xtick.set_fontsize(kSize)
    for ytick in ax1.get_yticklabels():
        ytick.set_fontsize(kSize)



def xyPlot(**kwargs):
    """
    """
    # ================================================
    # INPUT STAGE
    # ================================================

    ### Assign input arguments.
    filename = opt['input']
    uncertf = opt['uncert']
    doSubsample =  opt['subsample']
    num_groups = opt['group']

    if opt['mean'] != 0:
        doMean = True
        mean_period = int(opt['mean'])
    if doSubsample and 'doMean' in locals():
        sys.exit("You can subsample data or take the running average, but not both.")

    ### Read in data from file.
    data = np.loadtxt(filename)
    if uncertf is not None:
        uncerts = np.loadtxt(uncertf)
    x = data[:,0]

    ### Check that first column of uncertainties match first column of data
    # TODO!

    ### Get the y-columns.
    if opt['columns'] is not None:
        cols = list(map(int,opt['columns'].split(';')))
        y_mat = np.asarray([data[:,i] for i in cols]).T
        if uncertf is not None:
            uncerts = np.asarray([uncerts[:,i] for i in cols]).T
    else:
        y_mat = data[:,1:]
        if uncertf is not None:
            uncerts = uncerts[:,1:]

    # get number of columns in orig data set
    num_cols = y_mat.shape[1]
    if num_cols == 1:
        y_mat = y_mat.flatten()

    ### If data is broken up for subplots, only works for single column data.
    if num_groups != 0:

        if num_cols != 1:
            sys.exit("ERROR: This script is not equipped to break input "
                     "data into groups with multiple data columns.")

        if opt['legend'] is not None:
            print("WARNING: Input legend will be discarded. Grouped data will "
                  "instead be labeled by group count.")

        y_mat = np.array_split(y_mat, num_groups) # LIST of subarrays, may not be equally split
        num_cols = len(y_mat) # actually is number of groups split up from the 1 column

    print("How many data series to plot: {}".format(num_cols))

    # ================================================
    # PROCESSING STAGE
    # ================================================

    ### subsample data (may not want to if not timeseries data!)
    if doSubsample:
        x_mat, y_mat = subsample(x, y_mat, num_cols)

    elif 'doMean' in locals(): # if False, doMean variable does not exist
        y_mat = moving_average(y_mat,mean_period,num_cols)

        # since x and y are not 1:1 due to computing moving average,
        # regenerate x data based on scaling factor, e.g., to convert
        # frame number to ns.
        scale_x = 0.02
        try:
            x = scale_x * np.asarray(range(len(y_mat[0])), dtype=np.float32)
        except TypeError:
            x = scale_x * np.asarray(range(len(y_mat)), dtype=np.float32)

    # ================================================
    # PLOTTING STAGE
    # ================================================

    ### Define cmap color map.
    #colors = mpl.cm.tab20(np.linspace(0, 1, num_cols))
    colors = mpl.cm.tab20(np.linspace(0, 1, 10))
    #colors = mpl.cm.Dark2(np.linspace(0, 1, 8))

    num_plots = 1
    if num_groups != 0:
        factors = factorize(num_groups)
        num_plots = int(input("\nInput with {} data points will be separated "
              "into {} groups for plotting.\nDo you want to separate these "
              "groups into separate subplots?\nType 1 for no, or type an "
              "integer for the number of subplots desired.\nTo evenly distribute "
              "the lines, use one of {}. ".format(len(x),num_groups,factors)))
        lines_per_plot = int(num_groups/num_plots)

        # color map
        colors = mpl.cm.tab10(np.linspace(0, 1, 10))
        #colors = mpl.cm.bwr(np.linspace(0, 1, lines_per_plot))

    ### Initialize figure.
    fig, axs = plt.subplots(1, num_plots, sharey=True)
    if num_plots == 1:
        curr_ax = axs
    else:
        idx = 0
        opt['legend'] = ';'.join(str(i) for i in range(1,1+lines_per_plot))
        curr_ax = axs[idx]

    for i in range(num_cols):

        ### Determine which data to plot.
        if num_groups != 0: # most specific case
            y = y_mat[i]
            x = np.arange(len(y))
            c = colors[i % lines_per_plot]

            if (num_plots != 0) and (i > 0) and (i % lines_per_plot == 0):
                idx += 1

                # format the current subplot then get next legend ready
                format_fig(curr_ax, plt, fig, **opt)
                opt['legend'] = ';'.join(str(i) for i in range(i+1, i+1+lines_per_plot))

                # change to next subplot
                print("Switching to new subplot...")
                curr_ax = axs[idx]

        elif num_cols == 1:
            y = y_mat
            c = colors[i]

        elif doSubsample:
            y = y_mat[i]
            x = x_mat[i]
            c = colors[i]

        elif 'doMean' in locals():
            y = y_mat[i]
            c = colors[i]

        else:
            y = y_mat[:,i]
            c = colors[i]

        ### Plot the data.
        plot_args = {'color':c, 'lw':1.0, 'alpha':0.8}
        print(i, len(x), y.shape)

        if uncertf is not None:
            curr_ax.errorbar(x, y, yerr=uncerts[:,i], capsize=1.5, **plot_args)
        else:
            curr_ax.plot(x, y, **plot_args)

            # add points with the line plot
            #curr_ax.scatter(x, y, **plot_args, s=2)

    ### Format figure.
    axes = plt.gca()

    if num_groups != 0:
        plt.subplots_adjust(wspace=0.)

    format_fig(curr_ax, plt, fig, **opt)

    ### Save figure.
    if opt['publish']:
        plt.savefig(opt['output'], bbox_inches='tight', dpi=300)
    else:
        plt.savefig(opt['output'], bbox_inches='tight')
    plt.show()


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()

    # DATA INPUT
    parser.add_argument("-i", "--input",
                        help="Name of the input file.")
    parser.add_argument("-u", "--uncert", default=None,
                        help="Name of the file with corresponding uncertainties"
                        + ". Not compatible with moving averages or subsampling.")
    parser.add_argument("-c", "--columns", default=None,
                        help="Specify particular data columns to plot. Separate"
                        " values with semicolon and place in quotes (bc bash). "
                        "Ex. \"2;3;4\". The 0th column is x, so don't specify "
                        "0. If not specified, will plot all data columns.")
    parser.add_argument("-g", "--group", default=0, type=int,
                        help="If specified, break the data up into this many "
                        " groups to plot separately. E.g., a datafile might"
                        " be 100 lines long but you may want to plot 5 lines of"
                        " 20. Then use an argument of 5.")

    # DATA PROCESSING
    parser.add_argument("-m", "--mean", default=0, type=int,
                        help="If not default=0, take moving averages over the "
                        + "specified number of data points for each column.")
    parser.add_argument("-s", "--subsample", action="store_true",default=False,
                        help="Subsample y data based on correlation times.")

    # PLOT LABELING AND FORMATTING
    parser.add_argument("-x", "--xlabel", default="",
                        help="Label for x data.")
    parser.add_argument("-y", "--ylabel", default="",
                        help="Label for y data.")
    parser.add_argument("-t", "--title", default="",
                        help="Label for plot title.")
    parser.add_argument("-l", "--legend", default=None, type=str,
                        help="Add legend to data. Format input as "
                        "\"data1;data2;...\" with quotes. User-supplied legend"
                        " is currently not compatible with grouped data. If "
                        "--group is specified, use a placeholder (e.g., x) "
                        "here to label by count of group.")
    parser.add_argument("-o", "--output",
                        help="Name of the output figure.")
    parser.add_argument("--publish", action="store_true",default=False,
                        help="Reduce figure/font sizes for publications.")

    args = parser.parse_args()
    opt = vars(args)
    xyPlot(**opt)
