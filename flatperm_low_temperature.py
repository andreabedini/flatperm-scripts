#!/home/abedini/new-polymers-env/bin/python


import sys
import os.path
sys.path.append(os.path.expanduser('~/Dropbox/Polymers/analisys/'))

import matplotlib.pyplot as plt

import numpy as np
import tables
from . import flatperm

title = 'low temperature'

def compute(w, hfs):
    size = hfs[0].root.sW.shape[0]
    kw = { 'start': 100, 'stop': size, 'step': 50 }
    n = np.arange(**kw)
    Ps = np.array([1 - 2 * flatperm.avO(
                hf.root.sW.read(**kw), hf.root.m2W.read(**kw), w)
                   / n for hf in hfs])
    return n, Ps.mean(0), Ps.std(0)

def plot(w, hfs):
    n, y, yerr = compute(w, hfs)
    plt.errorbar(n**-0.5, y, yerr = yerr, label = r'$\omega = %.1f$' % w)

def do_plot(hfs):
#    plot(1.5, hfs)
#    plot(2.0, hfs)
#    plot(2.5, hfs)
    plot(7, hfs)

    plt.xlim(xmin = 0, xmax = 0.1)
    plt.ylim(ymin = 0, ymax = 1)
    plt.xlabel(r'$n^{-1/2}$')
    plt.ylabel(r'$p_n$')
    plt.legend(loc = 4)

    fn = '{}.pdf'.format(title.replace(' ', '_'))
    print(('saving figure in ' + fn))
    plt.savefig(fn)

if __name__ == '__main__':
    do_plot([ tables.openFile(f) for f in sys.argv[1:]] )
