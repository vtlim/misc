
"""
polar_plot.py

Purpose: Plot histogram of a given angle on a polar coordinate plot.
  Options: (1) scatter plot, (2) histogram of angle.

Example:    python polar_plot.py -i test.dat [-j test1.dat test2.dat]

Version:    Mar 12 2019
By:         Victoria T. Lim
"""

import os, sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import argparse

def load_file(filename):
    data = np.loadtxt(filename)
    times = data[:,0]
    angles = data[:,1]
    angles = np.radians(angles)

    return times, angles

def polar_hist(filename, filelist=[], bins_number=72):
    """
    Reference: https://tinyurl.com/y9wzfo6f
    """

    # load data
    times, angles = load_file(filename)
    # create bins and specify bin widths
    bins = np.linspace(0.0, 2 * np.pi, bins_number + 1)
    width = 2 * np.pi / bins_number
    # histogram data into equally-sized bins and get n=values of bins
    n, _, _ = plt.hist(angles, bins)

    # repeat with filelist if not empty
    nlist = []
    for f in filelist:
        _, angles = load_file(f)
        x, _, _ = plt.hist(angles, bins)
        nlist.append(x)

    # replot the histograms to center bins (e.g., center at 0 instead of start at 0)
    plt.clf()
    ax = plt.subplot(111, projection='polar')
    colors = mpl.cm.Set1(np.linspace(0, 1, 10))
    # IF you have a single histogram & want a diff color, chg index of colors[]
    bars = ax.bar(bins[:bins_number], n, width=width, bottom=0.0,color=colors[0])
    for bar in bars:
        bar.set_alpha(0.5)

    # repeat with filelist if not empty
    for i, f in enumerate(filelist):
        bars = ax.bar(bins[:bins_number], nlist[i], width=width, bottom=0.0, color=colors[i+1])
        for bar in bars:
            bar.set_alpha(0.5)
    # IF you want to change the histogram range, do so here
    ax.set_ylim(0,100)

    for xtick in ax.get_xticklabels():
        xtick.set_fontsize(18)
    plt.savefig('output.png')
    plt.show()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input",
                        help="File with timeseries data. Time in first column,"
                             " measurement in second column. # = commented.")
    parser.add_argument("-j", "--jnput", nargs='*',
                        help="Data to histogram separately, in diff. colors. "
                             "Specify 1+ files here separated by space.")
    args = parser.parse_args()
    opt = vars(args)

    # make sure input file is specified AND exists
    if not opt['input'] or not os.path.exists(opt['input']):
        sys.exit("\nERROR: Specify a valid input file.\n")
    # check additional files if specified
    if opt['jnput']:
        for f in opt['jnput']:
            if not os.path.exists(f):
                sys.exit("\nERROR: File '{}' not found.\n".format(f))
    else:
        opt['jnput'] = []

    polar_hist(opt['input'], opt['jnput'])
