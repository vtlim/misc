#!/usr/bin/python

import matplotlib.pyplot as plt
import numpy as np

def plot_hists(infiles):
    colors=['firebrick','darkorange','gold','limegreen','royalblue','darkorchid']
    colors.reverse()

    num_files = len(infiles)

    alldata = []
    for i in infiles:
        data = np.loadtxt(i)[:,1]
        alldata.append(data)

    fig, axs = plt.subplots(num_files, 1, sharex=True, tight_layout=True, figsize=(5,8))
    for i, d in enumerate(alldata):
        # if there's only one file, can't call axs[i] so put in list
        try:
            axs[i]
        except TypeError:
            axs = [axs]
        axs[i].hist(d,range=[-1,1], bins=100, color=colors[i])
        axs[i].axvline(x=0,color='silver',linestyle='--')

    plt.savefig('output.png')
    plt.show()


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()

    parser.add_argument("-i", "--infile", nargs='+',
                        help="Name of the input file(s).")

    args = parser.parse_args()
    plot_hists(args.infile)
