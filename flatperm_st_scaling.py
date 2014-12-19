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

title = 'specific heat scaling'

def do_plot(hf):
    s = hf.title + "\n"
    att = hf.root._v_attrs
    for a in att._v_attrnamesuser:
        s = s + "{}: {}\n".format(a, att[a])

    ax = plt.figure().add_subplot(111)
    w = np.linspace(0, 5, 1000)
    for i in range(-1, -501, -100):
        n = hf.root.sW.shape[0] + i
        wpeak = hf.root.st_peak.cols.wpeak[n]
        cwidth = hf.root.st_peak.cols.cwidth[n]
        x = (w - wpeak) / cwidth
        cpeak = hf.root.st_peak.cols.cpeak[n]
        y = flatperm.C(hf.root, n)(w) / cpeak
        ax.plot(x, y, label = r'$n = %d$' % n)

    ax.set_xlim(-1.5, 1.5)
    ax.set_ylim(0, 1.2)
    ax.set_xlabel(r'$(\omega-\omega_{c,n})/\Delta c_n$')
    ax.set_ylabel(r'$c_{n}(\omega) / c_n(\omega_{c,n})$')
    ax.set_title('{}: {}'.format(hf.title, title))
    ax.legend(loc = 0)
    ax.text(0.95, 0, s, transform = ax.transAxes, ha = 'right')
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
