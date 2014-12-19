#!/usr/bin/env python


import sys
import os.path
sys.path.append(os.path.expanduser('~/Dropbox/Polymers/analisys/'))

from . import bestfit
import numpy as np
import pylab as plt
from tables import openFile

title = 'gamma exponent'

def do_plot(hf):
    ax = plt.figure().add_subplot(111)

    Z = hf.root.sW[:]
    i = np.arange(Z.shape[0]/2 + 1)
    x = np.log2(i)
    y = np.log2(Z[2*i]/Z[i]**2)

    ax.plot(x, y)
    res = bestfit.leastsq(x, y, data_range = x > 6)

    res['line'].set_label('slope = %.3f' % res['slope'])
        
    ax.set_xlim(xmin = 5)
    ax.set_xlabel(r'$\log_2\ n$')
    ax.set_ylabel(r'$\log_2\ Z_{2n}/Z_n^2$')
    ax.set_title('{}: {}'.format(hf.title, title))

    ax.legend(loc = 0)
    basename = os.path.splitext(os.path.basename(hf.filename))[0]
    fn = '{}.{}.pdf'.format(basename, title.replace(' ', '_'))
    print(('saving figure in ' + fn))
    plt.savefig(fn)

if __name__ == '__main__':
    from contextlib import closing
    for filename in sys.argv[1:]:
        with closing(openFile(filename)) as hf:
            do_plot(hf)
            
