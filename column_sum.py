#!/usr/bin/python

# Sum input columns as a new series and write out file.

import numpy as np

def sumSeries(**kwargs):

    ### Read in data from file.
    filename = opt['input']
    data = np.loadtxt(filename)
    x = data[:,0]

    ### Get the y-columns.
    if opt['columns'] is not None:
        cols = list(map(int,opt['columns'].split(';')))
        y_mat = np.asarray([data[:,i] for i in cols]).T
    else:
        y_mat = data[:,1:]
    num_cols = y_mat.shape[1] # how many columns in orig data set
    if num_cols == 1: y_mat = y_mat.flatten()

    ### Loop over y-columns
    newdata = y_mat.sum(axis=1)

    # Save output.
    together = np.array([x, newdata]).T
    np.savetxt(opt['output'], together)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()

    parser.add_argument("-i", "--input",
                        help="Name of the input file. First line is assumed "
                        "to be some heading line and is NOT read in.")
    parser.add_argument("-c", "--columns",default=None,
                        help="Specify particular data columns to sum. Separate"
                        " values with semicolon and place in quotes (bc bash). "
                        "Ex. \"2;3;4\". The 0th column is x, so don't specify "
                        "0. If not specified, will sum all data columns.")
    parser.add_argument("-o", "--output",
                        help="Name of the output file.")

    args = parser.parse_args()
    opt = vars(args)
    sumSeries(**opt)
