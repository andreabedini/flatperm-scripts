



import numpy as np
import fast_bincount

def walk(g, k):
    data = g.table[g.index[k]:g.index[k+1]]
    return np.array(zip(*data)[2])

def point_square(x):
    return np.sum(np.square(x))

def Re2(w):
    return point_square(w[-1])

def Rg2(w):
    return np.average(list(map(point_square, w - np.average(w,0))))

def Rm2(w):
    return np.average(list(map(point_square, w)))

def compute_radius(group):
    s = None
    Re2 = []
    Rg2 = []
    Rm2 = []
    for r in group.table:
        if r['s'] != s:
            s = r['s']
            w1 = np.zeros(2)
            w2 = 0

        n = r['n']
            
        w1 += r['x']
        w2 += point_square(r['x'])

        Re2.append( point_square(r['x']) )
        Rg2.append( w2 / n - point_square(w1 / n) )
        Rm2.append( w2 / n )

    res = np.core.records.fromarrays([Re2, Rg2, Rm2],
                                     names = ['Re2', 'Rg2', 'Rm2'])
    
    group._v_file.createTable(group, 'radius', res)

def radius_stats(group):
    nmax= group._v_attrs['N']
    Re2 = np.zeros(nmax + 1)
    Rg2 = np.zeros(nmax + 1)
    Rm2 = np.zeros(nmax + 1)

    for t, r in zip(group.table, group.radius):
        Re2[t['n']] += r['Re2']
        Rg2[t['n']] += r['Rg2']
        Rm2[t['n']] += r['Rm2']

    if 'Re2' in group: group.Re2._f_remove()
    if 'Rg2' in group: group.Rg2._f_remove()
    if 'Rm2' in group: group.Rm2._f_remove()

    group._v_file.createArray(group, 'Re2', Re2)
    group._v_file.createArray(group, 'Rg2', Rg2)
    group._v_file.createArray(group, 'Rm2', Rm2)
    
def stats(table):
    p = fast_bincount.bincount(table['n'])
    n = p.nonzero()[0]
    p = p[n]

    _n = table['n']
    _m2 = table['m2'].astype(np.uint64)
    _m3 = table['m3'].astype(np.uint64)
    
    kG = np.log(25.0/3) / np.log(5./3)
    _m = _m2 + kG * _m3

    m2 = fast_bincount.bincount(_n, _m2).astype(np.double)[n]
    m3 = fast_bincount.bincount(_n, _m3).astype(np.double)[n]
    m2sq = fast_bincount.bincount(_n, _m2 ** 2).astype(np.double)[n]
    m3sq = fast_bincount.bincount(_n, _m3 ** 2).astype(np.double)[n]

    u2 = m2 / p / n
    u3 = m3 / p / n
    c2 = ((m2sq / p) - (m2 / p)**2) / n
    c3 = ((m3sq / p) - (m3 / p)**2) / n

    m = fast_bincount.bincount(_n, _m).astype(np.double)[n]
    msq = fast_bincount.bincount(_n, _m ** 2).astype(np.double)[n]
        
    u = m / p / n
    c = ((msq / p) - (m / p)**2) / n

    names = ['n', 'u2', 'c2', 'u3', 'c3', 'u', 'c']
    return np.core.records.fromarrays([n, u2, c2, u3, c3, u, c],
                                      names = names)

if __name__ == '__main__':
    if 'analysis' in hf.root:
        print("erasing old analysis")
        hf.removeNode(hf.root.analysis, recursive = True)

        s = stats(hf.root.table.read())

        group = hf.createGroup('/', 'analysis')
        hf.createArray(group, 'u2', s.u2)
        hf.createArray(group, 'u3', s.u3)
        hf.createArray(group, 'c2', s.c2)
        hf.createArray(group, 'c3', s.c3)
        hf.createArray(group, 'u', s.u)
        hf.createArray(group, 'c', s.c)
        hf.createArray(group, 'n', s.n)


