#!/usr/bin/env python

from contextlib import closing

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

import argparse
import os.path
import sys
import pylab as plt
import numpy as np
from tables import openFile

title = 'samples stats enr pru'

def do_plot(hf, show = True):
    s = hf.title + "\n"
    att = hf.root._v_attrs
    for a in att._v_attrnamesuser:
        s = s + "{}: {}\n".format(a, att[a])

    ax = plt.figure().add_subplot(111)
    ax.plot(np.log10(hf.root.Enr[:]), label=r'$\log_{10}\ Enr$')
    ax.plot(np.log10(hf.root.Pru[:]), label=r'$\log_{10}\ Pru$')
    ax.set_xlabel(r'$n$')
    ax.set_ylim(ymin = 1)
    ax.set_title('{}: {}'.format(hf.title, title))
    ax.text(0.95, 0.5, s, transform = ax.transAxes, ha = 'right')
    ax.legend(loc = 0)

    basename = os.path.splitext(os.path.basename(hf.filename))[0]
    fn = '{}.{}.pdf'.format(basename, title.replace(' ', '_'))
    print(('saving figure in ' + fn))
    plt.savefig(fn)

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
        do_plot(hf, show = args.show)
