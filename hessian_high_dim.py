import numpy as np

def weight(os, ws):
    A = np.multiply.reduce([w ** (o - o.mean()) for o, w in zip(os, ws)])
    return A / A.sum()

def hessian(Z):
    ndim = Z.ndim

    A = np.sum(Z)
    o = np.ix_(*list(map(range, Z.shape)))

    B = np.zeros((ndim, ndim))
    for i, j in np.ndindex(ndim, ndim):
        if i >= j: B[j, i] = B[i, j] = np.sum(Z * o[i] * o[j])/A 

    C = np.zeros((ndim, ndim))
    for i, j in np.ndindex(ndim, ndim):
        if i >= j: C[j, i] = C[i, j] = np.sum(Z * o[i])/A * np.sum(Z * o[j])/A

    return B - C

def hessian_weighted(Z, ws):
    obs = np.ix_(*list(map(range, Z.shape)))
    return hessian(Z * weight(obs, ws))

# x = y = z = np.linspace(0.1, 10, 10)

def hessian_vectorized(Z, args):
    dims = [ A.size for A in args ] + [len(args), len(args)]
    H = np.empty(dims, 'double')
    H.flat = [ hessian_weighted(Z, ws) for ws in itertools.product(*args) ]
    return H

def max_eigenvalue(H):
    E = np.array([ np.linalg.eigvalsh(H[ij]).max() for ij in np.ndindex(H.shape[:-2]) ])
    return E.reshape(H.shape[:-2])

# os = np.ix_(*map(range, Z.shape))

# H = np.empty((x.size, y.size, z.size, 2, 2), Z.dtype)
# H.flat = [ hessian(Z * weight(os, (a,b,c))) for a in x for b in y for c in z ]

# E = np.array([ np.linalg.eigvalsh(H[i,j,k]).max() for i,j,k in np.ndindex(H.shape[:-2]) ]).reshape(H.shape[:-2])

def chunk_list(lst, chunk_size):
    """Split a list into multiple lists of length chunk_size"""
    return [lst[i:i+chunk_size] for i in range(0, len(lst), chunk_size)]

def function_dechunker(func):
    """Return a function that processes ``func`` over a list of elements"""
    def wrapper_inner(chunked_args):
       # Regular Python map runs serially within job
       return list(map(func, chunked_args))
    return wrapper_inner

import itertools

def grouper(iterable, n, fillvalue=None):
    "Collect data into fixed-length chunks or blocks"
    # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx
    args = [iter(iterable)] * n
    return itertools.zip_longest(fillvalue=fillvalue, *args)

import cloud
import os

def save_online(Z, name):
    from tempfile import TemporaryFile
    outfile = TemporaryFile()
    np.save(outfile, Z)
    outfile.seek(0)
    cloud.bucket.putf(outfile, name)

def _hessian_on_the_cloud(name, ws_list):
    print("loading")
    Z = np.load(os.path.join('/bucket', name))
    print("computing")
    return [ hessian_weighted(Z, ws) for ws in ws_list ]

def hessian_on_the_cloud(name, args, chunk_size = 500):
    print("submitting")
    dims = [ A.size for A in args ] + [len(args), len(args)]
    H = np.empty(dims, 'double')
    ws_product_chunked = grouper(itertools.product(*args), chunk_size)
    jids = cloud.map(lambda ws: _hessian_on_the_cloud(name, ws), ws_product_chunked)
    print("waiting")
    chunked_results = cloud.result(jids)
    print("assembling")
    H.flat = list(itertools.chain.from_iterable(chunked_results))
    return H
