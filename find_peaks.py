#!/usr/bin/env python
from .tools import read_and_normalize
import numpy as np
from progressbar import ProgressBar
from itertools import groupby

def _group(a):
    i = 0
    r = []
    for k, g in groupby(a):
        l = len(list(g))
        r.append( (k, i, l) )
        i = i + l
    return r

def _top(a, ratio = 0.8):
    return a > ratio * a.max()

def _filter(groups, cutoff = 5):
    new_groups = []
    for g in groups:
        if not new_groups:
            new_groups.append(g)
        else:
            last = new_groups[-1]
            if g[2] < cutoff or g[0] == last[0]:
                new_groups[-1] = (last[0], last[1], last[2] + g[2])
            else:
                new_groups.append(g)
    return new_groups

def find_peaks(dist, **kwargs):
    peaks = []
    groups = _filter(_group(_top(dist['W'])))
    for v, x, l in [v for v in groups if v[0]]:
        block = slice(x, x + l)
        x = dist['W'][block].argmax()
        peaks.append( (dist['W'][block][x], dist['m'][block][x]) )
    return peaks

def find_double2(dist, a = None, b = None):
    n = dist.cols.n[:]
    if not a: a = n.min()
    if not b: b = n.max()

    s = 1
    l = [False]
    while not any(l):
        s = s * 2
        g = (find_peaks(dist.readWhere('n == %d' % n)) for n in range(a, b, (b-a)/s))
        l = [len(l) > 1 for l in g]
        print((a, b, s))
    i = l.index(True)
    print((list(range(a, b, (b-a)/s))[i]))

def normalize(x):
    return x / np.sum(x)

def fourth_moment(x, w):
    x0 = np.average(x, weights=w)
    a = np.average((x - x0)**4, weights=w)
    b = np.average((x - x0)**2, weights=w)**2
    return a / b

def unpack_by_field(dist, field):
    col = dist.colinstances[field]
    col.is_indexed or col.createCSIndex()
    
    a = np.min(col[:])
    b = np.max(col[:])
    
    for n in range(a, b+1):
        yield n, dist.readWhere('%s == %d' % (field, n))

def find_double_peaks(dist, *args, **kwargs):
    peaks = []
    
    if not dist.cols.n.is_indexed:
        print('Indexing...')
        dist.cols.n.createCSIndex()
    
    pbar = ProgressBar(maxval = len(dist))
    iterargs = dict(e for e in list(kwargs.items()) if e[0] == 'start' or e[0] == 'stop')
    for n, g in groupby(pbar(dist.itersorted('n', **iterargs)), lambda r: r['n']):
        rs = np.array([r.fetch_all_fields() for r in g], dtype=dist.dtype)
        r = find_peaks(rs, *args, **kwargs)
        if len(r) > 1:
            peaks.append((n, r))
    
    if peaks:
        l = np.array(zip(*zip(*zip(*peaks)[1])[0])[0])
        r = np.array(zip(*zip(*zip(*peaks)[1])[1])[0])
        i = abs(l / r - 1).argmin()

        width = max(zip(*peaks)[0]) - min(zip(*peaks)[0]) 

        dist.attrs.peaks = peaks
        dist.attrs.double_peak = peaks[i]
        dist.attrs.double_peak_region_width = width

    return peaks

if __name__ == '__main__':
    import sys
    import tables
    
    filename = sys.argv[1]
    hf = tables.openFile(filename, 'r+')
    print(filename)
    if find_double_peaks(hf.root.m2dist):
        print(('m2 peak: ', hf.root.m2dist.attrs.double_peak))
        print(('m2 peak region: ', hf.root.m2dist.attrs.double_peak_region_width))
    if find_double_peaks(hf.root.m3dist):
        print(('m3 peak: ', hf.root.m3dist.attrs.double_peak))
        print(('m3 peak region: ', hf.root.m3dist.attrs.double_peak_region_width))
    hf.close()
