#!/usr/bin/env python


import sys
# import os.path
# sys.path.append(os.path.expanduser('~/Dropbox/Polymers'))

import argparse

from scipy.optimize import bisect
from .fmin import fmin

import numpy as np
import tables

from . import flatperm
from progressbar import ProgressBar

import cloud
import itertools

def do_one(Z):
    x0, _ = fmin(lambda w: -flatperm.st(Z, w), 1.0)
    omega_max, tr_max = fmin(lambda w: -flatperm.tr(Z, w), x0)
    omega_min, tr_min = fmin(lambda w:  flatperm.tr(Z, w), x0)
    return omega_max, -tr_max, omega_min, tr_min

def compute(sW):
    n = np.arange(sW.shape[0])

    omega_max = np.zeros_like(n, dtype=np.double)
    omega_min = np.zeros_like(n, dtype=np.double)
    tr_max    = np.zeros_like(n, dtype=np.double)
    tr_min    = np.zeros_like(n, dtype=np.double)

    pbar = ProgressBar()

    for i, Z in enumerate(pbar(sW)):
        omega_max[i], tr_max[i], omega_min[i], tr_min[i] = do_one(Z)

    names = 'omega_max max omega_min min'.split()
    return np.rec.fromarrays([omega_max, tr_max, omega_min, tr_min],
                             names = names)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Find the peaks of the tri momentum for each size.')
    parser.add_argument('filename', nargs = '+', action = 'store')
    parser.add_argument('--force', action='store_true')
    
    try:
        args = parser.parse_args()
    except:
        parser.print_help()
        sys.exit()
    
    for fn in args.filename:
        with tables.openFile(fn, 'r+') as hf:
            if args.force or not 'tr_peak' in hf.root:
                r = compute(hf.root.sW[:])
                if 'tr_peak' in hf.root:
                    hf.root.tr_peak._f_remove()
                hf.createTable('/', 'tr_peak', r,
                               title = 'extensive third derivative')
                print((hf.filename, 'done.'))

            else:
                print((hf.filename, ': tr_peak present use --force to recompute'))
