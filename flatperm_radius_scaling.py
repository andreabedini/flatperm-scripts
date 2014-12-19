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

title = 'radius scaling'

def do_plot(hf):
    s = hf.title + "\n"
    att = hf.root._v_attrs
    for a in att._v_attrnamesuser:
        s = s + "{}: {}\n".format(a, att[a])

    ax = plt.figure().add_subplot(111)

    n = np.arange(hf.root.st_peak.shape[0], dtype=np.double)
    w = hf.root.st_peak.cols.wpeak[:]

    Re2 = flatperm.Re2(hf.root)
    r2 = np.array([ Re2(y, x)[0]
                    for x, y in zip(n, w) ], dtype=np.double)

    ax.plot(np.log(n), 0.5 * np.log(r2), label = r'$\omega = \omega_{c,n}$')
    res = bestfit.leastsq(np.log(n), 0.5 * np.log(r2), data_range = n > 100,
                          axes = ax)
    
    res['line'].set_label('slope = %.3f' % res['slope'])
    
    ax.set_xlabel(r'$\log\ n$')
    ax.set_ylabel(r'$1/2\ \log\ \langle R^2 \rangle$')
    ax.set_title('{}: {}'.format(hf.title, title))
    ax.legend(loc = 0)
    ax.text(0.98, 0.02, s, transform = ax.transAxes,
            ha = 'right', va = 'bottom')
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
