#!/usr/bin/env python

from contextlib import closing
from os.path import expanduser
import sys
sys.path.append(expanduser('~/Polymers/code/analisys'))

import numpy as np
from scipy.optimize import leastsq

from progressbar import ProgressBar, FileTransferSpeed, \
    Bar, Percentage, ETA 

def do_histogram(dist, shape, mu = 1):
    print(('reading %s' % dist._v_name))

    print(shape)

    X1 = np.zeros(shape, dtype=np.double)
    X2 = np.zeros(shape, dtype=np.double)
    X3 = np.zeros(shape, dtype=np.double)
    X4 = np.zeros(shape, dtype=np.double)
    
    print('computing ... ')

    widgets = [FileTransferSpeed(), ' ', Bar(), ' ',
               Percentage(), ' ', ETA()]

    pbar = ProgressBar(widgets=widgets)
    
    lmu = np.log(mu)

    for row in pbar(dist):
        n, x, W = row.fetch_all_fields()
        W = np.exp(np.log(W) - n * lmu)
        X1[n] += W * x 
        X2[n] += W * x ** 2
        X3[n] += W * x ** 3
        X4[n] += W * x ** 3

    return np.column_stack([X1,X2,X3,X4])

def do_file(filename):
    import tables
    with closing(tables.openFile(filename, 'r')) as hf:
        mu_eff = (hf.root.sW[1:]/hf.root.sW[:-1]).astype(float)
        mu_fit = leastsq(lambda p: p[0] - mu_eff, [1])[0]

        print(('normalization is ', mu_fit))

        dists = [ node for node in hf.iterNodes('/', classname='Table')
                  if '_dist' in node.name ]

        shape = hf.root.sW.shape
        for dist in dists:
            u, c, t = do_histogram(dist, shape, mu_fit)

            variable_name = dist.name.split('_')[0]

            group_name = variable_name + '_analysis'
            if group_name in hf.root:
                group = hf.getNode(hf.root, group_name)
            else:
                group = hf.createGroup(hf.root, group_name)
            
            if 'u' in group: hf.removeNode(group, 'u')
            u_array = hf.createArray(group, 'u', u)
            u_array.title = variable_name + ' energy'

            if 'c' in group: hf.removeNode(group, 'c')
            c_array = hf.createArray(group, 'c', c)
            c_array.title = variable_name + ' specific heat'

            if 't' in group: hf.removeNode(group, 't')
            c_array = hf.createArray(group, 't', t)
            c_array.title = variable_name + ' third cumulant'

if __name__ == '__main__':
    import sys
    for filename in sys.argv[1:]:
        print(('elaborating stats for %s' % filename))
        do_file(filename)
        
