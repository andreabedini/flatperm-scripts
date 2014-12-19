#!/home/abedini/new-polymers-env/bin/python


import sys
import os.path
sys.path.append(os.path.expanduser('~/Dropbox/Polymers/analisys/'))

import matplotlib.pyplot as plt

import numpy as np
import tables
from . import flatperm

title = 'specific heat shape'

def compute(w, hfs):
    n = hfs[0].root.sW.shape[0]
    Ps = np.array([flatperm.C(hf.root, -1)(w) / n for hf in hfs])
    return Ps.mean(0), Ps.std(0) / np.sqrt(Ps.shape[0])

def plot(w, hfs):
    y, yerr = compute(w, hfs)
    plt.errorbar(w, y, yerr = yerr)

def do_plot(hfs):
    w = np.linspace(1, 3, 100)
    plot(w, hfs)

    plt.xlim(1, 3)
    plt.xlabel(r'$\omega$')
    plt.ylabel(r'$c_n(\omega)$')

    fn = '{}.pdf'.format(title.replace(' ', '_'))
    print(('saving figure in ' + fn))
    plt.savefig(fn)

if __name__ == '__main__':
    do_plot([ tables.openFile(f) for f in sys.argv[1:]] )
