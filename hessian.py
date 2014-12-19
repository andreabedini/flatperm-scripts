# -*- python -*-
import itertools
import pylab as plt
import numpy as np

def _hessian(lZ, o1, lw1, o2, lw2):
    np_sum = np.sum
    lW = lZ + o1 * lw1 + o2 * lw2
    W = np.exp(lW - lW.max() + np.log(1e300))
    A = np_sum(W)
    Wo1 = W * o1
    Wo2 = W * o2
    B = np_sum(Wo1) / A
    C = np_sum(Wo2) / A
    D = np_sum(Wo1 * o1) / A
    E = np_sum(Wo1 * o2) / A
    F = np_sum(Wo2 * o2) / A
    a = D - B*B
    b = E - B*C
    c = F - C*C
    H = np.empty((2,2))
    H.flat = (a, b, b, c)
    return H

# largest eigenvalue
def eigh(H):
    eva = np.empty([H.shape[0], H.shape[1]], dtype=H.dtype)
    eve = np.empty([H.shape[0], H.shape[1], 2], dtype=H.dtype)
    for ij in np.ndindex(H.shape[0:2]):
        va, ve = np.linalg.eigh(H[ij])
        eva[ij] = np.max(va)
        eve[ij] = ve[np.argmax(va)]
    return eva, eve

def hessian(Z, w1, w2):
    H = np.empty([w1.size, w2.size, 2, 2], Z.dtype)
    o1, o2 = np.indices(Z.shape, np.double)
    lZ = np.log(Z)
    lw1 = np.log(w1)
    lw2 = np.log(w2)
    H.flat = [ _hessian(lZ, o1, x, o2, y) for x in lw1 for y in lw2 ]
    return H

## TO BE REWRITTEN with a simpler iteration

# def grid_block(x, y, size = 5):
#     ix_blocks = np.array_split(x, size)
#     iy_blocks = np.array_split(y, size)
#     return itertools.product(ix_blocks, iy_blocks)

# def spawn_jobs(x, y, f):
#     ii, jj = zip(*grid_block(np.arange(x.size), np.arange(y.size)))
#     jids = cloud.map(lambda i, j: f(x[i], y[j]), ii, jj)
#     return zip(ii, jj, jids)

# def result(jobs):
#     return [ (xx, yy, cloud.result(jid)) for xx, yy, jid in jobs ]

# def reconstruct(w1, w2, res):
#     elshape = res[0][2][0,0].shape
#     eldtype = res[0][2][0,0].dtype
#     R = np.empty((w1.size, w2.size) + elshape, eldtype)
#     idx = np.arange(R.size).reshape(R.shape)
#     for i, j, r in res:        
#         k, l = np.ix_(i, j)
#         np.put(R, idx[k, l].flatten(), r)
#     return R

# def cloud_submit(Z, w1, w2):
#     jobs = spawn_jobs(w1, w2, lambda x, y: hessian(Z, x, y))
#     return reconstruct(w1, w2, result(jobs))

def plot(H, w1, w2):
    eva, eve = eigh(H)
    Y, X = np.meshgrid(w2, w1)
    plt.contourf(X, Y, np.log(eva), 50)
    plt.colorbar()
    plt.xlabel(r'$\omega_1$')
    plt.ylabel(r'$\omega_2$')
    plt.title('greatest eigenvalue of second derivatives (log scale)')
