#!/usr/bin/env python

import argparse
import tables
import sys
import numpy as np

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='merge flatperm simulations outputs')
    parser.add_argument('--output', dest = 'outfile', action = 'store', required=True)
    parser.add_argument('a', action = 'store')
    parser.add_argument('b', action = 'store')

    try:
        args = parser.parse_args()
    except:
        parser.print_help()
        sys.exit()

    print(("INPUT : ", args.a, args.b))
    print(("OUTPUT: ", args.outfile))

    filters = tables.Filters(complevel = 1)
    
    with tables.openFile(args.outfile, 'a', filters=filters) as hfo, \
            tables.openFile(args.a) as hfa, \
            tables.openFile(args.b) as hfb:
        
        keys = [ node.name for node in hfa.listNodes('/', classname='Array') ]

        for k in keys:
            print(k)
            if not k in hfo.root:            
                hfo.createArray('/', k, np.subtract(
                        hfa.getNode('/', k).read(),
                        hfb.getNode('/', k).read() ))
            else:
                print('skipping...')
                
        hfo.title = hfa.title
                
