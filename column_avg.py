#!/usr/bin/python

# Take average and stdev of input columns.

import numpy as np

def column_avg(**kwargs):

    ### Read in data from file.
    filename = opt['input']
    data = np.loadtxt(filename)

    ### Get the columns.
    if opt['columns'] is not None:
        cols = list(map(int,opt['columns'].split(';')))
        y_mat = np.asarray([data[:,i] for i in cols]).T
    else:
        y_mat = data[:,0:]
    num_cols = y_mat.shape[1] # how many columns in orig data set

    ### Loop over columns and take stats.
    avgs = np.mean(y_mat, axis=0)
    stds = np.std(y_mat, axis=0)
    print(avgs, stds)

    # Save output.
    if opt['output']:
        with open(filename, 'a') as f:
            f.write("# Avgs: {}\n".format(avgs))
            f.write("# Stds: {}\n".format(stds))


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()

    parser.add_argument("-i", "--input",
                        help="Name of the input file. Comments denoted with #")
    parser.add_argument("-c", "--columns",default=None,
                        help="Specify particular data columns to avg. Separate"
                        " argument with semicolon and place in quotes (bc bash). "
                        "Ex. \"2;3;4\". If not specified, will avg all columns.")
    parser.add_argument("-o", "--output",action="store_true",default=False,
                        help="Write output as comments at end of file?")

    args = parser.parse_args()
    opt = vars(args)
    column_avg(**opt)
