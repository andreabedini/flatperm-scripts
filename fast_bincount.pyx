# -*- python -*-
from __future__ import division

import numpy as np
cimport numpy as np

def bincount(x, W = None):
    x = x.astype(np.uint64)
    if W == None:
        W = np.ones_like(x)

    if W.dtype.kind == 'u':
        return _bincount_integer(x, W.astype(np.uint64))
    if W.dtype.kind == 'f':
        return _bincount_double(x, W.astype(np.double))

cdef _bincount_integer(np.ndarray[np.npy_uint64, ndim=1] samples, np.ndarray[np.npy_uint64, ndim=1] weights):
    max_index = samples.max()
    cdef np.ndarray[np.npy_uint64, ndim=1] h = np.zeros(max_index + 1, dtype=np.uint64)
    cdef Py_ssize_t i = 0
    cdef Py_ssize_t imax = samples.shape[0]
    for i in range(imax):
        h[samples[i]] += weights[i]
    return h

cdef _bincount_double(np.ndarray[np.npy_uint64, ndim=1] samples, np.ndarray[np.npy_double, ndim=1] weights):
    max_index = samples.max()
    cdef np.ndarray[np.npy_double, ndim=1] h = np.zeros(max_index + 1, dtype=np.double)
    cdef Py_ssize_t i = 0
    cdef Py_ssize_t imax = samples.shape[0]
    for i in range(imax):
        h[samples[i]] += weights[i]
    return h
