#!/usr/bin/env python


import sys
# import os.path
# sys.path.append(os.path.expanduser('~/Dropbox/Polymers'))

import argparse

from scipy.optimize import bisect
from .fmin import fmin

import numpy as np
import tables

from .flatperm import st
from progressbar import ProgressBar

def do_one(Z):
    x, y = fmin(lambda w: -st(Z, w), 1.0)
    x0, x1 = 0.01, 20 * x
    l = bisect(lambda w: -st(Z, w) - y/2, x0, x)
    r = bisect(lambda w: -st(Z, w) - y/2, x, x1)
    return x, -y, r - l

def compute(sW):
    n = np.arange(sW.shape[0])

    wpeak  = np.zeros_like(n, dtype=np.double)
    cpeak  = np.zeros_like(n, dtype=np.double)
    cwidth = np.zeros_like(n, dtype=np.double)

    pbar = ProgressBar()

    for i, Z in enumerate(pbar(sW)):
        wpeak[i], cpeak[i], cwidth[i] = do_one(Z)

    names = 'wpeak cpeak cwidth'.split()
    return np.rec.fromarrays([wpeak, cpeak, cwidth],
                             names = names)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Find the specific heat peak for each size.')
    parser.add_argument('filename', nargs = '+', action = 'store')
    parser.add_argument('--force', action='store_true')

    try:
        args = parser.parse_args()
    except:
        parser.print_help()
        sys.exit()
    
    for fn in args.filename:
        with tables.openFile(fn, 'r+') as hf:
            if args.force or not 'st_peak' in hf.root:
                r = compute(hf.root.sW[:])
                if 'st_peak' in hf.root:
                    hf.root.st_peak._f_remove()
                hf.createTable('/', 'st_peak', r,
                               title = 'extensive specific heat')
                print((hf.filename, 'done.'))
            else:
                print((hf.filename, ': st_peak present use --force to recompute'))
