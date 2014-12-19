#!/usr/bin/env python


import sys
from os.path import expanduser
sys.path.append(expanduser('~/Dropbox/Polymers/analisys/'))

from contextlib import closing
import argparse
import os.path

import matplotlib.pyplot as plt

import numpy as np
from tables import openFile

from . import flatperm
from scipy.optimize import leastsq

title = 'gamma estimate vs omega'

def do_plot(hf):
    s = hf.title + "\n"
    att = hf.root._v_attrs
    for a in att._v_attrnamesuser:
        s = s + "{}: {}\n".format(a, att[a])

    ax = plt.figure().add_subplot(111)

    Z = flatperm.Z(hf.root)
    f_omega = lambda w, l: 1 + np.log2(Z(w, 2 * l) / Z(w, l)**2) / np.log2(2.0 / l)

    # # 
    # n = np.arange(hf.root.st_peak.shape[0])
    # wpeak = hf.root.st_peak.cols.wpeak[:]
    # p = leastsq(lambda p: p[0] + p[1] * n[100:] ** p[2] - wpeak[100:],
    #             [1,1,-1])[0]

    # print 'infinite length critical temperature = %.4f' % p[0]
    # print 'shift exponent = %.4f' % p[2]

    l = np.arange(100, hf.root.sW.shape[0] / 2 + 1, 100)

    # from scipy.optimize import fmin
    # f = lambda w: np.std(f_nu(w, l))
    # w_cross = fmin(f, p[0])[0]

    # print 'crossing temperature = %.4f' % w_cross

#    w = np.linspace(-1, 1, 100) + w_cross
    w = np.linspace(1, 6, 1000)
    w_, l_ = np.ix_(w, l)

    res = f_omega(w_, l_)

    lines = plt.plot(w, res)

    # nu_cross = np.mean(f_nu(w_cross, l))
    
    # s += r"$\omega$ crossing: %.3f" % w_cross + "\n"
    # s += r"$\nu$ crossing: %.3f" % nu_cross + "\n"

    for x, y in zip(lines, l):
        x.set_label('$n = %d$' % y)

    # ax.set_xlim(w_cross - 0.1, w_cross + 0.1)
    # ax.set_ylim(nu_cross - 0.1, nu_cross + 0.1)
    ax.set_xlabel(r'$\omega$')
    ax.set_ylabel(r'$1 + \log_2 \left(Z_{2n}(\omega)/Z_{n}^2(\omega)\right)/\log_2(2/n)$')
    ax.set_title('{}: {}'.format(hf.title, title))
    ax.legend(loc = 3)
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
