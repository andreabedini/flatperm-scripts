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

title = 'radius scaling log'

def do_plot(hf, show = True):
    s = hf.title + "\n"
    att = hf.root._v_attrs
    for a in att._v_attrnamesuser:
        s = s + "{}: {}\n".format(a, att[a])

    ax = plt.figure().add_subplot(111)

    n = hf.root.st_peak_scaling.cols.n[:]
    w = hf.root.st_peak_scaling.cols.wpeak[:]

    r2 = np.array([ flatperm.avO(hf.root.sW[x], hf.root.r2W[x], y)[0]
                    for x, y in zip(n, w) ])

    res = bestfit.leastsq(np.log(n), r2/(n*np.log(n)), n > 100,
                          data_label = r'$\omega = \omega_{c,n}$')
    
    for r in res:
        r['line'].set_label('slope = %.3f' % r['slope'])
    
    ax.set_xlabel(r'$\log\ n$')
    ax.set_ylabel(r'$\langle R^2 \rangle / \left(n \log\ n \right)$')
    ax.set_title('{}: {}'.format(hf.title, title))
    ax.legend(loc = 0)
    ax.text(0.05, 0.05, s, transform = ax.transAxes, ha = 'left')
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
