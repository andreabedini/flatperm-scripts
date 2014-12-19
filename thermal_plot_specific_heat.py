#!/usr/bin/env python


import sys
from os.path import expanduser
sys.path.append(expanduser('~/Dropbox/Polymers/analisys/'))

import os.path

import matplotlib.pyplot as plt

import numpy as np
from tables import openFile

title = 'specific heat'

def do_plot(hf, observable):
    s = "{} {}\n".format(hf.title, observable)
    att = hf.root._v_attrs
    for a in att._v_attrnamesuser:
        s = s + "{}: {}\n".format(a, att[a])

        
    data = hf.getNode('/', observable)
    A = data[:,2]/data[:,0]
    B = data[:,1]/data[:,0]
    C = A - B**2
    n = np.arange(C.shape[0])
    
    ax = plt.figure().add_subplot(111)
    ax.plot(C/n, label=r'{}/n'.format(observable))
    ax.set_xlabel(r'$n$')
    ax.set_ylabel(r'$C({})$'.format(observable))
    ax.set_title('{}: {}'.format(hf.title, title))

    ax.legend(loc = 0)
    ax.text(0.98, 0.02, s, transform = ax.transAxes,
            ha = 'right', va = 'bottom')
    basename = os.path.splitext(os.path.basename(hf.filename))[0]
    fn = '{}.{}.{}.pdf'.format(basename, title.replace(' ', '_'), observable)
    print(('saving figure in ' + fn))
    plt.savefig(fn)

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--observable', action = 'store')
    parser.add_argument('filename', action = 'store')

    try:
        args = parser.parse_args()
    except:
        parser.print_help()
        sys.exit()
        
    from contextlib import closing
    with closing(openFile(args.filename)) as hf:
        do_plot(hf, args.observable)
