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

title = 'energy density'

def do_plot(hf, weight, show = True):
    s = hf.title + "\n"
    att = hf.root._v_attrs
    for a in att._v_attrnamesuser:
        s = s + "{}: {}\n".format(a, att[a])

    n = hf.root.sW.shape[0] - 1
    m = np.arange(hf.root.sW.shape[1]).astype(float)

    ax = plt.figure().add_subplot(111)
    for w in weight:        
        ax.plot(m/n, flatperm.dist(hf.root.sW[n], w),
                label = r'$\omega = %.3f$' % w)

    ax.set_xlabel(r'$m/n$')
    ax.set_ylabel(r'$p(m/n)$')
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
    parser.add_argument('--weight', nargs = '+', action = 'store', type=float)
    parser.add_argument('--show', action = 'store_true')

    try:
        args = parser.parse_args()
    except:
        parser.print_help()
        sys.exit()

    with closing(openFile(args.filename)) as hf:
        if args.weight:            
            do_plot(hf, weight = args.weight, show = args.show)
        else:
            w = hf.root.st_peak_scaling.cols.wpeak[-1]
            do_plot(hf, weight = [w], show = args.show)
