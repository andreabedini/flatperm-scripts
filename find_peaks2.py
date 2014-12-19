def bla(dist, n):
    a = dist.readWhere('n == %d' % n)
    plot(a['m'], a['W']/a['W'].sum())
    il = find(np.cumsum(a['W']) < a['W'].sum()/2)
    ir = find(np.cumsum(a['W']) > a['W'].sum()/2)
    print((il, ir))
    ilmax = il[a['W'][il].argmax()]
    irmax = ir[a['W'][ir].argmax()]
    print((ilmax, irmax))
    mlmax = a['m'][ilmax]
    mrmax = a['m'][irmax]
    print((mlmax, mrmax))
    Wlmax = a['W'][ilmax]
    Wrmax = a['W'][irmax]
    print((Wlmax, Wrmax))
    print((Wrmax / a['W'][ir][0])) 

def _measure(dist, n):
    W = dist.readWhere('n == %d' % n, field = 'W')
    ir = np.argmax(np.cumsum(W) > W.sum()/2)
    return W[ir:].max() / W[ir]

def _define_region(dist):
    return [ n for n in np.unique(dist.cols.n[:]) if _measure(dist, n) > 1.5 ]

def analyze(dist):
    l = _define_region(dist)
    if l:
        a = min(l)
        b = max(l)
        dist._v_attrs['double_peak_region_begin'] = a
        dist._v_attrs['double_peak_region_end'] = b
        dist._v_attrs['double_peak_region_width'] = b - a
        print((a, b))
    else:
        print('empty')

