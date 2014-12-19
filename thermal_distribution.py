import numpy as np

def p(dist, n):
    sel = dist.readWhere('n == %d' % n)
    m = sel['m'].astype(float) / n
    W = sel['W']
    W = (W / W.sum() * n).astype(float)
    return np.core.rec.fromarrays([m, W], names = ['m', 'W'])
