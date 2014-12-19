#!/usr/bin/env python

import argparse
import tables
import sys
import numpy as np

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='merge flatperm simulations outputs')
    parser.add_argument('--output', dest = 'outfile', action = 'store', required=True)
    parser.add_argument('infiles', nargs = '+', action = 'store')

    try:
        args = parser.parse_args()
    except:
        parser.print_help()
        sys.exit()

    print(("INPUT : ", args.infiles))
    print(("OUTPUT: ", args.outfile))

    filters = tables.Filters(1)
    hfo = tables.openFile(args.outfile, 'a', filters=filters)
    hfs = [ tables.openFile(f, 'r') for f in args.infiles ]

    keys = [ node.name for node in hfs[0].listNodes('/', classname='Array') ]

    for k in keys:
        print(k)
        if k in hfo.root:
            print('skipping...')
            continue

        shape = hfs[0].getNode('/', k).shape
        atom = hfs[0].getNode('/', k).atom
        
        X = np.zeros(shape, atom.dtype)
        Y = np.zeros(shape, atom.dtype)
        for h in hfs:
            h.getNode('/', k).read(out = Y)
            np.add(X, Y, X)

        hfo.create_array('/', k, X)
        hfo.flush()

    for a in hfs[0].root._v_attrs._v_attrnamesuser:
        if a == 'time':
            continue
        print(a)
        hfo.root._v_attrs[a] = hfs[0].root._v_attrs[a]

    hfo.title = hfs[0].title
    
    hfo.close()
    for h in hfs:
        h.close()
