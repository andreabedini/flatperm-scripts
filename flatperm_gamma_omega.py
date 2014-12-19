#!/usr/bin/env python


import sys
import os.path

sys.path.append(os.path.expanduser('~/Dropbox/Polymers/analisys/'))

import matplotlib.pyplot as plt

import numpy as np
from tables import openFile

from . import flatperm

title = 'gamma vs omega'

def do_plot(hf, *args, **kwargs):
    ax = plt.figure().add_subplot(111)

    w = np.linspace(1, 3, 100)
    l = np.arange(500, hf.root.sW.shape[0], 100)
    w_, l_ = np.ix_(w, l)

    Z = flatperm.Z(hf.root)
    res = np.log( Z(w_, l_) / Z(w_, l_/2)**2 ) / np.log(l_/2)

    lines = plt.plot(w, res)
    for x, y in zip(lines, l):
        x.set_label('$n = %d$' % y)

    ax.set_xlim(1, 3)
    ax.set_ylim(-0.5, 1)
    ax.set_xlabel(r'$\omega$')
    ax.set_ylabel(r'$\log \left[Z_n(\omega)/Z_{n/2}(\omega)\right]/\log\ n$')
    ax.legend(loc = 0)

    basename = os.path.splitext(os.path.basename(hf.filename))[0]
    fn = '%s.%s.pdf' % (basename, title.replace(' ', '_'))
    print(('saving figure in ' + fn))
    plt.savefig(fn)

    zoom = kwargs.pop('zoom', None)
    if zoom:
        print(zoom)
        ax.set_xlim(zoom[0], zoom[1])
        ax.set_ylim(zoom[2], zoom[3])
        fn = '%s.%s.zoom.pdf' % (basename, title.replace(' ', '_')) 
        print(('saving figure in ' + fn))
        plt.savefig(fn)

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', action = 'store')
    zoom_type = lambda s: list(map(float, tuple(s.split(','))))
    parser.add_argument('--zoom', type = zoom_type)

    try:
        args = parser.parse_args()
    except:
        parser.print_help()
        sys.exit()
    
    from contextlib import closing
    with closing(openFile(args.filename)) as hf:
        do_plot(hf, **vars(args))
