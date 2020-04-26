#!/usr/bin/python

import os
import matplotlib.pyplot as plt
import numpy as np

def plot_hists(infiles, same_ax=False):
    num_files = len(infiles)

    alldata = []
    for i in infiles:
        data = np.loadtxt(i)[:,1]
        alldata.append(data)

    if not same_ax:
        colors=['firebrick','darkorange','gold','limegreen','royalblue','darkorchid']
        colors.reverse()

        # set figure size
        fig, axs = plt.subplots(num_files, 1, sharex=True, tight_layout=True, figsize=(5,8))

        for i, d in enumerate(alldata):
            # if there's only one file, can't call axs[i] so put in list
            try:
                axs[i]
            except TypeError:
                axs = [axs]
            axs[i].hist(d, range=[-1,1], bins=100, color=colors[i])
            axs[i].axvline(x=0, color='silver', linestyle='--')

    else:
        for i, d in enumerate(alldata):
            # google hex codes
            colors = ['#ab30c4', '#f4b400', '#46bdc6', '#db4437', '#0f9d58', '#4285f4', '#ff6d00'][1:]

            # set figure size
            plt.gcf().set_size_inches(2, 6)

            # normalize so that sum of all bars = 1
            # https://stackoverflow.com/a/16399202
            plt.hist(d, range=[-1,1], bins=100, color=colors[i],
                weights=np.ones_like(d)/float(len(d)),
                label=os.path.splitext(infiles[i]), alpha=0.7,
                orientation='horizontal')

            plt.axvline(x=0, color='silver', linestyle='--')
            plt.legend(loc=4)
            plt.ylim(-1.4, 1.4)
            plt.gca().yaxis.tick_right()
            plt.xlabel("normalized counts", fontsize=14)
            plt.xticks(fontsize=10)
            plt.yticks(fontsize=14)


    plt.savefig('output.png', bbox_inches='tight')
    plt.show()


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()

    parser.add_argument("-i", "--infile", nargs='+',
                        help="Name of the input file(s).")

    parser.add_argument("--together", action="store_true", default=False,
                        help="Plot histogram on the same axes instead of "
                             "on different subplots")

    args = parser.parse_args()
    plot_hists(args.infile, args.together)
