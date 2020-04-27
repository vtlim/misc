
"""
Generate contour plots of data from .dx files generated in VMD.

By:         Justin C. Smith, Victoria T. Lim
Version:    27 April 2020

Example:
$ python dx_plot.py -i infile.dx -o outfile.png --view_dim x --view_dim_val 0

Resources:
- https://www.ks.uiuc.edu/Research/vmd/plugins/molfile/dxplugin.html

"""

import numpy as np
import matplotlib.pyplot as plt
from gridData import Grid

def dx_plot(infile, outfile, dim, dim_val):
    """
    """

    # load data from dx file
    data = Grid(infile)
    box_lens = []

    # print info from dx file
    print(f"Shape of grid data: {data.grid.shape}")
    for i in range(3):
        this_len = data.edges[i].shape[0] - 1
        box_lens.append(this_len)
        print(f"Shape of edge {i}: {this_len}")
    print(f"Origin: {data.origin}")
    print(f"Delta: {data.delta}")

    # prep list containing points to be contour plotted
    points = []

    # view from x to see the yz plane
    if dim == 'x':

        # iterate over z
        for zi in range(box_lens[2]):
            subpoints = []

            # iterate over y
            for yi in range(box_lens[1]):
                subpoints.append(data.grid[dim_val, yi, zi])

            points.append(subpoints)

    # view from y to see the xz plane
    elif dim == 'y':

        # iterate over z
        for zi in range(box_lens[2]):
            subpoints = []

            # iterate over x
            for xi in range(box_lens[0]):
                subpoints.append(data.grid[xi, dim_val, zi])

            points.append(subpoints)

    # view from z to see the xy plane
    elif dim == 'z':

        # iterate over y
        for yi in range(box_lens[1]):
            subpoints = []

            # iterate over x
            for xi in range(box_lens[0]):
                subpoints.append(data.grid[xi, yi, dim_val])

            points.append(subpoints)

    # generate plot
    plt.contourf(np.array(points))
    plt.savefig(outfile)
    plt.show()


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()

    parser.add_argument("-i", "--infile",
                        help="Name of input dx file")

    parser.add_argument("-o", "--outfile",
                        help="Name of output image file")

    parser.add_argument("-d", "--view_dim",
                        help="Dimension from which to view 2D potential; "
                             "valid options are 'x' 'y' 'z'")

    parser.add_argument("-w", "--view_dim_val", type=int,
                        help="Where on the view_dim dimension to generate "
                             "2D snapshot. E.g., if you have 100 points in x "
                             "dimension and you want to see the yz plane at "
                             "the halfway point in xrange, specify value of 50")

    args = parser.parse_args()
    dx_plot(args.infile, args.outfile, args.view_dim, args.view_dim_val)

