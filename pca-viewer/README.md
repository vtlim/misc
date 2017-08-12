

# pca_representation.ipynb notebook
By: Victoria Lim and Matthew Agee

## Objective
This script reads in a molecule and finds its best 2D representation (showing as much of it as possible in 2D).
The task is accomplished with principal component analysis.
*Status:* rough draft. Verified to work from manual input of xyz coordinates.

## TO DO
1. add in read / write functions
2. test on a better case of 2gbi
3. test on a nonplanar molecule
4. add images in examples directory showing before and after
5. convert to python script
6. make command line readable
   * ex: `python -i input.xyz -o output.xyz --depict` where this takes input and output files. The `--depict` flag may be specified True to save images of both sets of coordinates.
7. read/write functions for other file types (\*.sdf, \*.pdb, etc.)
   * use openeye python toolkit
8. Check to see that bond lengths and angles are retained in output coordinates.
9. Add functions to depict and save images.
