#!/usr/bin/env python


import sys
from os.path import expanduser
sys.path.append(expanduser('~/Dropbox/Polymers/analisys/'))

import os.path

import matplotlib.pyplot as plt

import numpy as np
import tables
from . import bestfit

title = 'radius exponent'

labels = { 'Re2' : r'\langle R_e^2 \rangle_n',
           'Rm2' : r'\langle R_m^2 \rangle_n',
           'Rg2' : r'\langle R_g^2 \rangle_n', }

def do_plot(hf, radius = 'Re2'):
    ax = plt.figure().add_subplot(111)

    data = getattr(hf.root, radius)
    
    n = np.arange(data.shape[0])
    R2 = data[:,1] / data[:,0]

    x = np.log(n)
    y = 0.5 * np.log(R2)
    
    obs_label = labels.get(radius) or radius
    ax.plot(x, y, label = r'${}$'.format(obs_label))

    res = bestfit.leastsq(x, y, data_range = (x>5),
                          include_zero = True)
    
    res['line'].set_label('slope %.3f' % res['slope'])

    ax.set_xlabel(r'$\log n$')
    ax.set_ylabel(r'$1/2\, \log\ {}$'.format(obs_label))
    ax.legend(loc = 0)
    basename = os.path.splitext(os.path.basename(hf.filename))[0]
    fn = '{}.{}.{}.pdf'.format(basename, title.replace(' ', '_'), radius)
    print(('saving figure in ' + fn))
    plt.savefig(fn)

if __name__ == '__main__': 
    for filename in sys.argv[1:]:
        with tables.openFile(filename) as hf:
            for radius in ['Re2', 'Rm2', 'Rg2' ]:
                do_plot(hf, radius)
