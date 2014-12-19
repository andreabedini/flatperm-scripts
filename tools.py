##
##
##

import numpy as np

epsilon = 4.9406564584124654e-324

######################################################################
## simpler versions that use directly the index of Z as observable
######################################################################

def my_mesh(A):
    return np.meshgrid(*list(map(xrange, reversed(A.shape))))

######################################################################
# two parameter flat perm statistics
######################################################################

def av2(Z, w1, w2, index = 0):
    o = np.indices(Z.shape, Z.dtype)[index]
    o1, o2 = np.indices(Z.shape, Z.dtype)[-2:]
    lW = np.log(Z) + o1 * np.log(w1) + o2 * np.log(w2)
    W = np.exp(lW - lW.max() + np.log(1e300))
    A = (W).sum(-1).sum(-1)
    B = (W * o).sum(-1).sum(-1)
    return B/A

def st2(Z, w1, w2, index = 0):
    o = np.indices(Z.shape, double)[index]
    o1, o2 = np.indices(Z.shape, double)[-2:]
    lW = np.log(Z) + o1 * np.log(w1) + o2 * np.log(w2)
    W = np.exp(lW - lW.max() + np.log(1e300))
    A = (W).sum(-1).sum(-1)
    B = (W * o).sum(-1).sum(-1)
    C = (W * o ** 2).sum(-1).sum(-1)
    return C/A - (B/A)**2

######################################################################

# def av(oW, w, Z, index = -1):
#     o = arange(Z.shape[index], dtype=Z.dtype)
#     lA = np.log(Z) + o * np.log(w)
#     lB = np.log(oW) + o * np.log(w)
#     lAmax = atleast_1d(lA.max(index))[:,newaxis]
#     lBmax = atleast_1d(lB.max(index))[:,newaxis]
#     A = np.exp(lA - lAmax).sum(index)
#     B = np.exp(lB - lBmax).sum(index)
#     return B/A * np.exp(lBmax - lAmax)[:,0]

def pdist(w, Z, index = -1):
    o = np.indices(Z.shape, Z.dtype)[index]
    lA = np.log(Z) + o * np.log(w)
    lAmax = lA.max()
    A = np.exp(lA - lAmax)
    return A / A.sum(-1)

######################################################################

def av_with_scale(oW, sd, Z, index = -1):
    avgo = [ av(oW[n], w, Z[n])[0] for n, w, _ in sd ]
    return rec.fromarrays([sd.n, avgo], names = ['n', 'o'])

######################################################################

######################################################################

# def scaling_plot(n, c):
#     figure()
#     plot(np.log(n), np.log(c), '.', label=r'$\np.log\ c^{peak}$')
#     _, n2 = array_split(n, 2)
#     _, c2 = array_split(c, 2)
#     a, b = polyfit(np.log(n2), np.log(c2), 1)
#     plot(np.log(n), a * np.log(n) + b, '-', label=r'$slope = %f$' % a, hold=1)
#     ylabel(r'$\np.log\ c^{peak}$')
#     xlabel(r'$\np.log n$')
#     legend(loc = 0)

######################################################################

# from the list at
# http://reference.wolfram.com/mathematica/tutorial/NDSolvePDE.html

def diff1(x):
    """ 1/3 h^2 f^{(3)} """
    return convolve(x, [3./2,-4./2,1./2], mode='valid')

def diff5(x):
    """ 1/30 h^4 f^{(5)} """
    return convolve(x, [-1./5,8./5,-8./5,1./5], mode='valid')

def diff12(x):
    """1/140 h^6 f^{(7)}"""
    return convolve(x, [1./23,-9./23,45./23,-45./23,9./23,-1./23], mode='valid')

##################################################

def bla(t, i):
    print(('trace ending at %d' % i))
    while i != -1:
        yield t[i]
        i = t[i][0]

def draw_trace(trace, title = None):
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d import Axes3D
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ps = [ tuple(r[1]) for r in trace ]

    ax.plot(*list(zip(*ps)))

    c = Counter(ps)
    doubly = [ p for p, n in list(c.items()) if n == 2 ]
    if doubly:
        ax.scatter(*list(zip(*doubly)), c = 'b', marker = 'o')

    triply = [ p for p, n in list(c.items()) if n == 3 ]
    if triply:
        ax.scatter(*list(zip(*triply)), c = 'r', marker = 'o')

    if title:
        ax.set_title(title)

def filter_size(t, n):
    return [ r.nrow for r in t.where('n == %d' % n) ]

def bla2(t):
    idx = filter_size(t, 500)
    order = list(reversed(argsort(t[idx], order = 'W')))[:5]
    for i in order:
        print((idx[i], t[idx[i]]))
        _, _, n, W, m1, m2, m3 = t[idx[i]]
        title = r'$n = %d, W = %e, m_2 = %d, m_3 = %d$' % (n, W, m2, m3)
        draw_trace(bla(t, idx[i]), title = title)

def normalize(x):
    return x / x.sum()

def two_peaks(dist):
    y = np.average(dist['m'], weights=dist['W'])
    L = dist['m'] < y
    H = dist['m'] > y
    w1 = dist['W'][L].max()
    w2 = dist['W'][H].max()
    x1 = dist['m'][L][np.argmin(dist['W'][L] < w1)]
    x2 = dist['m'][H][np.argmin(dist['W'][H] < w2)]
    return (x1, w1), (x2, w2), w1/w2

def read_and_normalize(dist, n):
    tmp = dist.readWhere('n == %d' % n)[['m', 'W']]
    W = normalize(tmp['W']) * n
    m = tmp['m'].astype(np.double) / n
    return np.rec.fromarrays([m, W], names = ['m', 'W'])

def moment(i, dist):
    return average(dist['m'] ** i, weights = dist['W'])

def d_test(obs, calc):
    delta = obs - calc
    return np.sum(np.diff(delta) ** 2) / np.sum(delta ** 2)

