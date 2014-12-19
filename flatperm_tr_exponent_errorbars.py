#!/usr/bin/env python


import sys
from os.path import expanduser
sys.path.append(expanduser('~/Dropbox/Polymers/analisys/'))

import matplotlib.pyplot as plt

import numpy as np
import tables

from . import flatperm
from . import bestfit

title = 'tr exponent'

def est(hf):
    n = np.arange(hf.root.tr_peak.shape[0])
    tr_peak_max = hf.root.tr_peak.cols.max[:]
    tr_peak_min = hf.root.tr_peak.cols.min[:]
    i = n[100::2]

    est_max = np.log2(tr_peak_max[i] / tr_peak_max[i / 2] / 2)
    est_min = np.log2(tr_peak_min[i] / tr_peak_min[i / 2] / 2)
    
    # spurious point
    # est_min[-16] = np.NaN
    # est_min[-17] = np.NaN

    return i, est_max, est_min

def compute(hfs):
    X = np.array([ est(hf) for hf in hfs ])
    return X.mean(0), X.std(0) / np.sqrt(X.shape[0])

def do_plot(hfs):
    (i, y_max, y_min), (_, y_max_err, y_min_err) = compute(hfs)

    plt.errorbar(i**(-3./7), y_max, yerr = y_max_err,
                 label = 'positive peak', ls = '', marker = '.')

    plt.errorbar(i**(-3./7), y_min, yerr = y_min_err,
                 label = 'negative peak', ls = '', marker = '.')
 

    res = bestfit.leastsq(i**(-3./7), y_max, #fit_range = i > 400,
                          include_zero = True)

    res = bestfit.leastsq(i**(-3./7), y_min, #fit_range = i > 400,
                          include_zero = True)

    plt.xlim(xmax = 0.12)
    plt.xlabel(r'$n^{-3/7}$')
    plt.ylabel(r'$\log_2(t_{c,n}/t_{c,n/2})$')
    plt.legend(loc = 1)
    
    fn = title.replace(' ', '_') + '.pdf'
    print(('saving figure in ' + fn))
    plt.savefig(fn)

if __name__ == '__main__':
    do_plot([ tables.openFile(f) for f in sys.argv[1:] ])
