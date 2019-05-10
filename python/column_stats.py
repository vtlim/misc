#!/usr/bin/python

"""
Purpose:    Take average/stdev or min/max of each of the specified columns.
By:         Victoria T. Lim
Version:    Dec 6 2018
Example:    python column_stats.py -i countClose1.dat -c "1;2;3" -o

"""

import numpy as np
import sys

def column_stats(args):

    ### Read in data from file.
    filename = args.infile
    data = np.loadtxt(filename)

    ### Get the columns.
    if args.columns is not None:
        cols = list(map(int,args.columns.split(';')))
        try:
            y_mat = np.asarray([data[:,i] for i in cols]).T
        except IndexError:
            sys.exit("ERROR: Index of specified columns is greater than number of columns in file.")
    else:
        y_mat = data[:,0:]
    num_cols = y_mat.shape[1] # how many columns in orig data set

    ### Loop over columns and take stats.
    avgs = np.mean(y_mat, axis=0)
    stds = np.std(y_mat, axis=0)
    np.set_printoptions(precision=4,suppress=True)
    print("# Avgs: {}".format(avgs))
    print("# Stds: {}\n".format(stds))

    ### Save output.
    if args.output:
        with open(filename, 'a') as f:
            f.write("# Avgs: {}\n".format(avgs))
            f.write("# Stds: {}\n".format(stds))

    ### Compute minimum and maximum values of column.
    if args.minmax:
        cmin = np.amin(y_mat, axis=0)
        cmax = np.amax(y_mat, axis=0)
        print("# Min: {}".format(cmin))
        print("# Max: {}\n".format(cmax))


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()

    parser.add_argument("-i", "--infile",
                        help="Name of the input file. Comments denoted with #")
    parser.add_argument("-c", "--columns",default=None,
                        help="Specify particular data columns to avg. First "
                        "column is considered index ZERO. Separate arguments "
                        "with semicolon and place in quotes (bc bash). "
                        "Ex. \"2;3;4\". If not specified, will avg all columns.")
    parser.add_argument("-o", "--output",action="store_true",default=False,
                        help="Write output as comments at end of file?")
    parser.add_argument("-m", "--minmax",action="store_true",default=False,
                        help="Compute minimum and maximum of each column "
                        "in addition to average and standard deviation.")

    args = parser.parse_args()
    column_stats(args)

