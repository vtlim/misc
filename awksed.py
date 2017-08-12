#!/usr/bin/env python

# By: Victoria T. Lim

import sys
import os
from shutil import copyfile

def awksed(**kwargs):

    if opt['placement'] is not None and opt['placement'] == 0:
        sys.exit("Placement of zero is not valid for append pattern.")
    if opt['input'] == opt['output']:
        copyfile(opt['input'],'temp')
        opt['input'] = 'temp'
    if opt['skip']==None:
        opt['skip']=0
    #opt['append'] = opt['append'].replace("\\n","\n")

    # handle environment variables
    try:
        opt['append'] = opt['append'].replace(opt['replace'],os.environ[opt['replace'][-1]])
    except TypeError:
        pass

    # search the file
    searchline = opt['search']
    indices = []
    with open(opt['input'],'r') as f:
        lines = f.readlines()  # mostly for inserting later
        for (i, line) in enumerate(lines):
            if searchline in line:
                indices.append(i)

    try:
        theplace = indices[int(opt['skip'])]+int(opt['placement'])
    except TypeError:
        sys.exit("fix me") 
    print("Inserting pattern in line ", theplace)
    lines.insert(theplace, opt['append'])

    # write out output with appended pattern
    with open(opt['output'], "w") as out_file:
        for line in lines:
            out_file.write(line)

    # if file writing is successful, remove temp file
    if opt['input'] == 'temp':
        os.remove('temp')


if __name__ == "__main__": 
    import argparse
    parser = argparse.ArgumentParser() 
    parser.add_argument("-i", "--input", 
                        help="Name of the input file.")
    parser.add_argument("-s", "--search", 
                        help="Reference pattern to search for in file.")
    parser.add_argument("-c", "--skip",
                        help="Skip how many findings of search pattern? " +
                       "If not specified, will only treat first search pattern "
                       "found. If skip=4, skip the first four instances of "
                       "search pattern, then apply append pattern. " +
                       "If skip=-1, apply append pattern to ALL patterns. TODO")
    parser.add_argument("-a", "--append", 
                        help="Text pattern to be added.") 
    parser.add_argument("-r", "--replace", 
                        help="Subpattern inside the append pattern which is "
                        + "a placeholder for some environment variable to be "
                        + "replaced. E.g. expand $angle defined in bash.")
    parser.add_argument("-p", "--placement", 
                        help="Where to place text pattern with reference to "+
                        "search pattern. +1 is after, -1 is before, -2 is "
                        " two lines before, etc. O is not valid.")
    parser.add_argument("-o", "--output", 
                        help="Name of the output file.")
 
    args = parser.parse_args() 
    opt = vars(args) 
    awksed(**opt) 

