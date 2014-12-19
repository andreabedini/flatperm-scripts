#!/usr/bin/env python

from contextlib import closing

import os.path
import sys
sys.path.append(os.path.expanduser('~/Polymers/code/analisys'))

import argparse
import numpy as np
from progressbar import ProgressBar

import pyximport
pyximport.install(setup_args={'include_dirs': [ np.get_include(), ] })

import tables

def do_file(hf, force):
    dists = hf.listNodes('/', classname='Table')

    extent = hf.root.sW.shape[0]
    for dist in dists:
        ca_name = dist.name.replace('_dist', '')
        ca_atom = dist.coldescrs['W']
        ca_shape = (extent, extent)
        if force or not ca_name in hf.root:
            if ca_name in hf.root:
                hf.removeNode('/', ca_name)
            ca = hf.createCArray('/', ca_name, atom=ca_atom, shape=ca_shape)
            print(('converting ', dist.name, ' into ', ca_name))
            pbar = ProgressBar()
            for r in pbar(dist):
                ca[r['n'], r['m']] = r['W']
            hf.flush()
        else:
            print((hf.filename, ': %s present use --force to replace' % ca_name))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', nargs = '+', action = 'store')
    parser.add_argument('--force', action='store_true')
  
    try:
        args = parser.parse_args()
    except:
        parser.print_help()
        sys.exit()
    
    for filename in args.filename:
        with closing(tables.openFile(filename, 'r+')) as hf:
            print(('elaborating stats for %s' % filename))
            do_file(hf, force = args.force)
        
