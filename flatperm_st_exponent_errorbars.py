#!/home/abedini/new-polymers-env/bin/python


import sys
import os.path
sys.path.append(os.path.expanduser('~/Dropbox/Polymers/analisys/'))

import matplotlib.pyplot as plt

import numpy as np
import tables

from . import flatperm
from . import bestfit

title = 'st exponent'

def est(hf):
    n = np.arange(hf.root.st_peak.shape[0])
    st_peak = hf.root.st_peak.cols.cpeak[:] / n
    i = n[100::4]
    est = np.log2( (st_peak[i] - st_peak[i/2]) / (st_peak[i/2] - st_peak[i/4]) )
    return i, est

def compute(hfs):
    Ps = np.array([est(hf) for hf in hfs])
    return Ps.mean(0), Ps.std(0) / np.sqrt(Ps.shape[0])

def do_plot(hfs): 
    (i, y), (_, yerr) = compute(hfs)
    plt.errorbar(i**(-3./7), y, yerr = yerr)

    res = bestfit.leastsq(i**(-3./7), y, fit_range = i > 200,
                          include_zero = True)

    plt.xlim(0, 0.12)
    plt.ylim(-0.2, 0)

    plt.xlabel(r'$n^{-3/7}$')
    plt.ylabel(r'$\log_2[(c_n - c_{n/2})/(c_{n/2} - c_{n/4})]$')

    fn = title.replace(' ', '_') + '.pdf'
    print(('saving figure in ' + fn))
    plt.savefig(fn)

if __name__ == '__main__':
    do_plot([ tables.openFile(f) for f in sys.argv[1:]] )
