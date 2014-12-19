# -*- python -*-
import itertools
import numpy as np

# from analisys import smooth

def my_mesh(A):
    return np.ix_(*list(map(range, A.shape)))

def dist(sW, w):
    o = np.arange(sW.shape[-1], dtype=np.longdouble)
    Z = sW * w ** o
    return Z / Z.sum(-1)

def pf(sW, w):
    "partition function"
    o = np.arange(sW.shape[-1], dtype=np.longdouble)
    Z = sW * w ** o
    return np.sum(Z, -1) / sW.flat[0]

def fe(sW, mu, w):
    "free energy"
    o = np.arange(sW.shape[-1], dtype=np.longdouble)
    n = np.arange(sW.shape[0],  dtype=np.longdouble)
    Z = sW * w ** o
    return np.log(np.sum(Z, -1) / sW.flat[0]) + n * np.log(mu)

def av(sW, w):
    "internal energy"
    o = np.arange(sW.shape[-1], dtype=np.longdouble)
    Z = sW * w ** o
    A = np.sum(Z, -1)
    np.multiply(Z, o, Z)
    B = np.sum(Z, -1)
    return B / A

def avO(sW, O, w):
    o = np.arange(sW.shape[-1], dtype=np.longdouble)
    A = np.sum(sW * w ** o, -1)
    B = np.sum(O * w ** o , -1)
    return B / A

def st(sW, w):
    "specific heat"
    o = np.arange(sW.shape[-1], dtype=np.longdouble)
    Z = sW * w ** o
    A = np.sum(Z, -1)
    np.multiply(Z, o, Z)
    B = np.sum(Z, -1)
    np.multiply(Z, o, Z)
    C = np.sum(Z, -1)
    return C / A - (B / A)**2

def tr(sW, w):
    "third derivative"
    o = np.arange(sW.shape[-1], dtype=np.longdouble)
    Z = sW * w ** o
    A = np.sum(Z, -1)
    np.multiply(Z, o, Z)
    B = np.sum(Z, -1)
    np.multiply(Z, o, Z)
    C = np.sum(Z, -1)
    np.multiply(Z, o, Z)
    D = np.sum(Z, -1)
    return D / A - 3 * C / A * B / A + 2 * (B / A)**3

######################################################################

######################################################################
# for two-parameter data

def _my_sum(a, count = 1):
    """sum over the last count indices efficiently"""
    shape = a.shape[:-count] + (-1,)
    return a.view().reshape(shape).sum(-1)

def _my_sum2(a, indices):
    perm = [ i for i in range(a.ndim) if i not in indices ] + [ i for i in range(a.ndim) if i in indices ]
    shape = [ a.shape[i] for i in range(a.ndim) if i not in indices ]
    return a.view().transpose(perm).reshape(shape + [-1,]).sum(-1)

def fix(sW, w, index):
    o = np.indices(sW.shape, dtype=np.longdouble)[index]
    Z = np.sum(sW * w ** o, index)
    return Z

def fix_two(sW, w1, index1, w2, index2):
    obs = np.ix_(*list(map(range, sW.shape)))
    o1 = obs[index1]
    o2 = obs[index2]
    Z = _my_sum2(sW * weight((o1,o2), (w1, w2)), (index1, index2))
    return Z

def cured_weight(o1, w1, o2, w2):
    A = w1 ** (o1 - o1.mean()) * w2 ** (o2 - o2.mean())
    return A / A.sum()

def cured_weight_2(o1, w1, o2, w2):
    lA = np.log(w1) * o1 + np.log(w2) * o2
    A = np.exp(lA - lA.max())
    return A / A.sum()

def weight(os, ws):
    A = np.multiply.reduce([w ** (o - o.mean()) for o, w in zip(os, ws)])
    return A / A.sum()

def avO_multi(sW, O, ws):
    obs = np.ix_(*list(map(range, sW.shape)))
    W = weight(obs, ws)
    A = _my_sum(sW * W, W.ndim)
    B = _my_sum(O  * W, W.ndim)
    return B / A

def hessian(Z):
    ndim = Z.ndim

    A = np.sum(Z)
    obs = np.ix_(*list(map(range, Z.shape)))

    B = np.zeros((ndim, ndim))
    for i, j in np.ndindex(ndim, ndim):
        if i >= j: B[j, i] = B[i, j] = np.sum(Z * obs[i] * obs[j])/A 

    C = np.zeros((ndim, ndim))
    for i, j in np.ndindex(ndim, ndim):
        if i >= j: C[j, i] = C[i, j] = np.sum(Z * obs[i])/A * np.sum(Z * obs[j])/A

    return B - C

def hessian_weighted(Z, ws):
    obs = np.ix_(*list(map(range, Z.shape)))
    return hessian(Z * weight(obs, ws))

def hessian_vectorized(Z, args):
    dims = [ A.size for A in args ] + [len(args), len(args)]
    H = np.empty(dims, 'double')
    H.flat = [ hessian_weighted(Z, ws) for ws in itertools.product(*args) ]
    return H

def max_eigenvalue(H):
    E = np.array([ np.linalg.eigvalsh(H[ij]).max() for ij in np.ndindex(H.shape[:-2]) ])
    return E.reshape(H.shape[:-2])

######################################################################

def make_convenience_adaptor_extensive(fn):
    def wrapper(hf, n = None):
        if n is None:
            sW = hf.getNode('/sW')[:]
            return np.vectorize(lambda w, n: fn(sW[n], w))
        else:
            sW = hf.getNode('/sW')[n,...]
            return np.vectorize(lambda w: fn(sW, w))
    wrapper.__doc__ = "extensive " + fn.__doc__
    return wrapper

Z = make_convenience_adaptor_extensive(pf)
F = make_convenience_adaptor_extensive(fe)
U = make_convenience_adaptor_extensive(av)
C = make_convenience_adaptor_extensive(st)
T = make_convenience_adaptor_extensive(tr)

def make_convenience_adaptor_reduced(fn):
    def wrapper(hf, n = None):
        if n is None:
            sW = hf.getNode('/sW')[:]
            return np.vectorize(lambda w, n: fn(sW[n], w) / n)
        else:
            sW = hf.getNode('/sW')[n,...]
            return np.vectorize(lambda w: fn(sW, w) / n)
    wrapper.__doc__ = "intensive " + fn.__doc__
    return wrapper

f = make_convenience_adaptor_reduced(fe)
u = make_convenience_adaptor_reduced(av)
c = make_convenience_adaptor_reduced(st)
t = make_convenience_adaptor_reduced(tr)

def O(name, hf, i = slice(None)):
    W = hf.getNode('/sW')[i,...]
    O = hf.getNode('/', name)[i,...]
    def _tmp(w, i_ = slice(None)):
        return avO(W[i_], O[i_], w)
    return np.vectorize(_tmp)

def O_critical(name, hf, i = slice(None)):
    W = hf.getNode('/sW')[i,...]
    O = hf.getNode('/', name)[i,...]
    wp = hf.getNode('/st_peak')[i]['wpeak']
    return avO(W, O, wp[:,None])

def O_critical_smooth(name, hf, i = slice(None)):
    W = hf.getNode('/sW')[i,...]
    O = hf.getNode('/', name)[i,...]
    n = np.arange(W.shape[0])[i,...]
    wp = hf.getNode('/st_peak')[i]['wpeak']
    wp_smooth = smooth(n, wp)
    return avO(W, O, wp_smooth[:,None])

def U2(hf, i = slice(None)):
    return O('m2W', hf, i)

def U3(hf, i = slice(None)):
    return O('m3W', hf, i)

def Re2(hf, i = slice(None)):
    return O('Re2W', hf, i)

def Rg2(hf, i = slice(None)):
    return O('Rg2W', hf, i)

def Rm2(hf, i = slice(None)):
    return O('Rm2W', hf, i)

def A(hf, i = slice(None)):
    _Rg2 = Rg2(hf, i)
    _Re2 = Re2(hf, i)
    @np.vectorize
    def _tmp(w, i = slice(None)):
        return _Rg2(w, i) / _Re2(w, i)
    return _tmp

def B(hf, i = slice(None)):
    _Rm2 = Rm2(hf, i)
    _Re2 = Re2(hf, i)
    @np.vectorize
    def _tmp(w, i = slice(None)):
        return _Rm2(w, i) / _Re2(w, i)
    return _tmp

def L(hf, i = slice(None)):
    _A = A(hf, i)
    _B = B(hf, i)
    @np.vectorize
    def _tmp(w, i = slice(None)):
        return (4 * _B(w, i) - 1) / (2 * _A(w, i))
    return _tmp
