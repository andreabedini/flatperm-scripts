#!/usr/bin/env python

from contextlib import closing

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

import argparse
import os.path
import sys
import numpy as np
import pylab as plt
from tables import openFile
from . import flatperm
from . import bestfit

title = 'energy at peak 4 7'

def do_plot(hf, show = True):
    s = hf.title + "\n"
    att = hf.root._v_attrs
    for a in att._v_attrnamesuser:
        s = s + "{}: {}\n".format(a, att[a])

    ax = plt.figure().add_subplot(111)

    n = hf.root.st_peak_scaling.cols.n[:]
    w = hf.root.st_peak_scaling.cols.wpeak[:]

    u = flatperm.U(hf.root)
    u_at_peak = np.array([u(y, x)[0] for x, y in zip(n, w) ])

    ax.plot(n**(-4./7), u_at_peak)

#    res = bestfit.leastsq(np.log(n), np.log(r2), n > 100,
#                          data_label = r'$\omega = \omega_{c,n}$')
    
#    for r in res:
#        r['line'].set_label('slope = %.3f' % r['slope'])

    ax.set_xlim(xmin = 0)
    ax.set_xlabel(r'$n^{-4/7}$')
    ax.set_ylabel(r'$u^p_n$')
    ax.set_title('{}: {}'.format(hf.title, title))
    ax.legend(loc = 0)
    ax.text(0.95, 0, s, transform = ax.transAxes, ha = 'right')
    basename = os.path.splitext(os.path.basename(hf.filename))[0]
    fn = '%s.%s.pdf' % (basename, title.replace(' ', '_'))
    print(('saving figure in ' + fn))
    plt.savefig(fn)
#    if show: plt.show()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', action = 'store')
    parser.add_argument('--show', action = 'store_true')

    try:
        args = parser.parse_args()
    except:
        parser.print_help()
        sys.exit()

    with closing(openFile(args.filename)) as hf:
        do_plot(hf)
