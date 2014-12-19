#!/usr/bin/env python


from contextlib import closing

import sys
import argparse
import os.path
from tables import openFile

def parse_key(hf, key):
    base, attr = os.path.split(key)
    node = hf.getNode('/', base)
    return node, attr

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Modify hdf5 attributes.')
    parser.add_argument('filename', action = 'store')
    group = parser.add_mutually_exclusive_group(required=True)

    group.add_argument('--set', nargs = 2, action='append', default=[])
    group.add_argument('--delete', action='append', default=[])
    group.add_argument('--get', action='append', default=[])
    
    try:
        args = parser.parse_args()
    except:
        parser.print_help()
        sys.exit()
    
    with closing(openFile(args.filename, 'r+')) as hf:
        for key, value in args.set:
            print(('set %s to %s' % (key, value)))
            node, attr = parse_key(hf, key)
            node._v_attrs[attr] = value
        
        for key in args.get:
            node, attr = parse_key(hf, key)
            print(('get %s = %s' % (key, node._v_attrs[key])))

        for key in args.delete:
            node, attr = parse_key(hf, key)            
            print(('delete %s' % key))
            del node._v_attrs[key]
        
