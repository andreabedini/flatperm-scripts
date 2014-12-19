#!/home/abedini/new-polymers-env/bin/python


import sys
import os.path
sys.path.append(os.path.expanduser('~/Dropbox/Polymers/analisys/'))

import matplotlib.pyplot as plt

import numpy as np
import tables

from . import flatperm
from . import bestfit
from . import estimators

title = 'crossover exponent from energy'

def est(hf):
    n = np.arange(hf.root.st_peak.shape[0])
    w_c = hf.root.st_peak.cols.wpeak[:]
    u_c = flatperm.av(hf.root.sW[:], w_c[:,None]) / n
    return estimators.convergent(n, u_c.astype(float))

def compute(hfs):
    Ps = np.array([est(hf) for hf in hfs])
    return Ps.mean(0), Ps.std(0)

def do_plot(hfs): 
    (i, y), (_, yerr) = compute(hfs)

    plt.errorbar(1./i, y + 1, yerr = yerr, ls = '.')
    res = bestfit.leastsq(1./i[10:], y[10:] + 1,
                          fit_range = 1./i[10:] < 0.01,
                          include_zero = True)
    res['line'].set_label('intercept {[intercept]:.3f}'.format(res))

    plt.legend(loc = 0)

    plt.xlim(0, 0.01)
    plt.ylim(0, 1)

    plt.xlabel(r'$1/n$')
    plt.ylabel(r'$\phi$')
    plt.title(title)
    
    fn = title.replace(' ', '_') + '.pdf'
    print(('saving figure in ' + fn))
    plt.savefig(fn)

if __name__ == '__main__':
    do_plot([ tables.openFile(f) for f in sys.argv[1:]] )
