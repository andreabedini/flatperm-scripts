#!/usr/bin/env python


import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.optimize import leastsq

from contextlib import closing
import argparse
import sys
import os.path
import numpy as np
from tables import openFile
from . import bestfit

title = 'tr peak shift'

def do_plot(hf, exponent = None):
    n = np.arange(hf.root.st_peak.shape[0], dtype=np.double)[100:]
    w_max = hf.root.tr_peak.cols.omega_max[100:]
    w_min = hf.root.tr_peak.cols.omega_min[100:]

    f = lambda p, x: p[0] + p[1] * x

    if exponent:
        p0 = [ w_max[-1], 1, -1 ]
        p, _ = leastsq(lambda p: w_max - f(p, n ** exponent), p0)
        
        print(p)
        
    else:
        print('guessing the exponent')
        p0 = [ w_max[-1], 1, -1 ]
        p, _ = leastsq(lambda p: w_max - f(p, n ** p[2]), p0)
        
        print(p)
        
    s = hf.title + "\n"
    att = hf.root._v_attrs
    for a in att._v_attrnamesuser:
        s = s + "{}: {}\n".format(a, att[a])

    # s = s + "shift exponent: %.3f\n" % -p[2]
    # s = s + "extrapolated critical temp: %.3f\n" % p[0]

    ax = plt.figure().add_subplot(111)
    ax.plot(n ** p[2], w_max, '.')
    ax.plot(n ** p[2], w_min, '.')

    # x = np.linspace(0, n[0] ** p[2])
    # y = f(p, x)

    # ax.plot(x, y, '-')

    ax.set_xlim(xmin = 0)
    ax.set_xlabel(r'$n^{%.3f}$' % p[2])
    ax.set_ylabel(r'$w_{c,n}$')
    ax.set_title('{}: {}'.format(hf.title, title))
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
    parser.add_argument('--exponent', action = 'store', type=float)

    try:
	args = parser.parse_args()
    except:
	parser.print_help()
	sys.exit()

    with closing(openFile(args.filename)) as hf:
	do_plot(hf, args.exponent)
