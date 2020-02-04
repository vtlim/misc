#!/usr/bin/python

"""
Purpose: From multiple files, with columns of
(1) independent variable (e.g., residue number), and
(2) dependent variable (e.g., computed value),
in which the (1) column for each file correspond,
combine all dependent variable columns into a single file,
and also create a new column of the average of the dependent columns.

By:         Victoria T. Lim
Version:    Feb 3 2020

"""

import numpy as np

def combine_and_avg(infiles, outfile):

    # load data, combine to single array, delete x columns
    arrays = [np.loadtxt(f) for f in infiles]
    combined = np.concatenate(arrays, axis=1)
    trimmed = np.delete(combined, np.s_[::2], 1)

    # calculate average across rows
    avg = np.mean(trimmed, axis=1)

    # generate new x column
    x = np.arange(0, trimmed.shape[0])

    # combine all columns together
    full = np.column_stack((x, trimmed, avg))

    # save output
    np.savetxt(outfile, full, fmt='%1.3f', delimiter='\t',
        header="Columns in order of x, y1, y2, ..., avg(y)")



if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()

    parser.add_argument("-i", "--infiles", nargs='+',
                        help="Name of the input file(s)")

    parser.add_argument("-o", "--outfile", default='output.dat',
                        help="Name of the output file.")

    args = parser.parse_args()

    combine_and_avg(args.infiles, args.outfile)
