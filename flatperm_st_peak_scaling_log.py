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

title = 'specific heat peak scaling log'

def do_plot(hf):
    n = np.arange(hf.root.st_peak.shape[0], dtype=np.double)
    cpeak = hf.root.st_peak.cols.cpeak[:]

    s = hf.title + "\n"
    att = hf.root._v_attrs
    for a in att._v_attrnamesuser:
        s = s + "{}: {}\n".format(a, att[a])

    ax = plt.figure().add_subplot(111)
    res = bestfit.leastsq(np.log(np.log(n)), np.log(cpeak), n > 250)
    for r in res:
        r['line'].set_label('slope = %.3f' % r['slope'])

    ax.set_xlabel(r'$\log\ \log\ n$')
    ax.set_ylabel(r'$\log\ c^{(peak)}_n$')
    ax.set_title(hf.title + ': specific heat peak')
    ax.legend(loc = 0)
    ax.text(0.8, 0, s, transform = ax.transAxes, ha = 'right')

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
