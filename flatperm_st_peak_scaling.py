#!/usr/bin/env python


import matplotlib.pyplot as plt

from contextlib import closing
import argparse
import sys
import os.path
import numpy as np
from tables import openFile
from . import bestfit

title = 'specific heat peak scaling'

def do_plot(hf):
    n = np.arange(hf.root.st_peak.shape[0], dtype=np.double)
    cpeak = hf.root.st_peak.cols.cpeak[:] / n

    s = hf.title + "\n"
    att = hf.root._v_attrs
    for a in att._v_attrnamesuser:
        s = s + "{}: {}\n".format(a, att[a])

    ax = plt.figure().add_subplot(111)
    ax.plot(np.log(n), np.log(cpeak))
    res = bestfit.leastsq(np.log(n), np.log(cpeak), #data_range = (n > 750),
                          axes = ax)
    res['line'].set_label('slope = %.3f' % res['slope'])

    ax.set_xlim(xmin = 2)
    ax.set_xlabel(r'$\log\ n$')
    ax.set_ylabel(r'$\log\ c^{(peak)}_n$')
    ax.set_title(hf.title + ': specific heat peak')
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
