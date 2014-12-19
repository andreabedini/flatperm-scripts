#!/usr/bin/env python


import sys
import os.path
sys.path.append(os.path.expanduser('~/Dropbox/Polymers/analisys/'))

import matplotlib.pyplot as plt

import numpy as np
import tables

from . import flatperm

title = 'nu vs omega'

def do_plot(hf, *args, **kwargs):
    zoom_default = ( hf.root.st_peak.cols.wpeak[-1] - hf.root.st_peak.cols.cwidth[-1],
                     hf.root.st_peak.cols.wpeak[-1] + hf.root.st_peak.cols.cwidth[-1] )
    zoom = kwargs.pop('zoom', zoom_default)
    w_min, w_max = zoom

    w = np.linspace(w_min, w_max, 500)
    l = np.arange(500, hf.root.sW.shape[0], 100)
    w_, l_ = np.ix_(w, l)

    r2 = flatperm.Re2(hf)
    res = np.log2(r2(w_, l_) / r2(w_, l_/2)) / 2

    lines = plt.plot(w, res)
    for x, y in zip(lines, l):
        x.set_label('$n = %d$' % y)

    plt.xlim(w_min, w_max)
    plt.xlabel(r'$\omega$')
    plt.ylabel(r'$1/2\, \log_2 \left[\langle R^2 \rangle_{n}(\omega)/\langle R^2 \rangle_{n/2}(\omega)\right]$')
    plt.legend(loc = 0)

    basename = os.path.splitext(os.path.basename(hf.filename))[0]
    fn = '.'.join([ basename, title.replace(' ', '_'), 
                    '_'.join(map(str, zoom)),
                    'pdf' ])
    print(('saving figure in ' + fn))
    plt.tight_layout()
    plt.savefig(fn)

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', action = 'store')
    float_tuple = lambda s: list(map(float, tuple(s.split(','))))
    parser.add_argument('--zoom', type = float_tuple)

    try:
        args = parser.parse_args()
    except:
        parser.print_help()
        sys.exit()
    
    with tables.openFile(args.filename) as hf:
        do_plot(hf, **vars(args))
