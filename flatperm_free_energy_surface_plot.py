#!/usr/bin/env python

from contextlib import closing

import argparse
import os.path
import numpy as np
import pylab as plt
import mpl_toolkits.mplot3d
from tables import openFile

def do_file(hf):
    assert(len(hf.root.sW.shape) == 2)
    ax = figure().add_subplot(111, projection='3d')
    
    fn = os.path.splitext(os.path.basename(hf.filename))[0] + '.radius.pdf'
    print(('saving figure in ' + fn))
    plt.savefig(fn)
    plt.show()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Plot the free energy surface')
    parser.add_argument('filename', action = 'store')
    
    try:
        args = parser.parse_args()
    except:
        parser.print_help()
        sys.exit()

    with closing(openFile(args.filename)) as hf:
        do_file(hf)
