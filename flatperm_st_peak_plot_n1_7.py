#!/usr/bin/env python


import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from contextlib import closing
import argparse
import sys
import os.path
import numpy as np
from tables import openFile
from . import bestfit

title = 'specific heat peak n1_7'

def do_plot(hf):
    n = np.arange(hf.root.st_peak.shape[0], dtype=np.double)
    c = hf.root.st_peak.cols.cpeak[:] / n

    s = hf.title + "\n"
    att = hf.root._v_attrs
    for a in att._v_attrnamesuser:
        s = s + "{}: {}\n".format(a, att[a])

    ax = plt.figure().add_subplot(111)

    res = bestfit.leastsq(ax, n**(-1./7), c, n > 250, include_zero = True,
                          ls = '', marker = '.')
    for r in res:
        r['line'].set_label('slope = %.3f, intercept = %.3f' % (r['slope'], r['intercept']))

    ax.set_xlim(xmin = 0)
    ax.set_xlabel(r'$n^{-1/7}$')
    ax.set_ylabel(r'$c^{(peak)}_n$')
    ax.set_title('{}: {}'.format(hf.title, title))
    ax.legend(loc = 0)
    ax.text(0.05, 0.05, s, transform = ax.transAxes,
            ha = 'left', va = 'bottom')
    basename = os.path.splitext(os.path.basename(hf.filename))[0]
    fn = '%s.%s.pdf' % (basename, title.replace(' ', '_'))
    print(('saving figure in ' + fn))
    plt.savefig(fn)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', action = 'store')

    try:
        args = parser.parse_args()
    except:
        parser.print_help()
        sys.exit()

    with closing(openFile(args.filename)) as hf:
        do_plot(hf)
