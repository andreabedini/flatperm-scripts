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

title = 'tr peak scaling'

def do_plot(hf):
    n = np.arange(hf.root.tr_peak.shape[0], dtype=np.double)
    tr_max = hf.root.tr_peak.cols.max[:] / n
    tr_min = -hf.root.tr_peak.cols.min[:] / n

    s = hf.title + "\n"
    att = hf.root._v_attrs
    for a in att._v_attrnamesuser:
        s = s + "{}: {}\n".format(a, att[a])

    ax = plt.figure().add_subplot(111)
    res = bestfit.leastsq(ax, np.log(n), np.log(tr_max), n > 750,
                          marker = '.', ls = '',
                          label = r'$\log\ \max_{\omega}\ t_n(\omega)$')
    res[0]['line'].set_label('slope = %.3f' % res[0]['slope'])

    res = bestfit.leastsq(ax, np.log(n), np.log(tr_min), n > 750,
                          marker = 'x', ls = '',
                          label = r'$\log\|\min_{\omega}\ t_n(\omega)|$')
    res[0]['line'].set_label('slope = %.3f' % res[0]['slope'])

    ax.set_xlim(xmin = 4)
    ax.set_xlabel(r'$\log\ n$')
    ax.set_title(hf.title + ': tr peak')
    ax.legend(loc = 0)
    ax.text(0.98, 0.98, s, transform = ax.transAxes,
            ha = 'right', va = 'top')

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
