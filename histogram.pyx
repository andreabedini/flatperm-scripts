# -*- python -*-

import cython

cimport numpy as np
import numpy as np
from progressbar import ProgressBar, FileTransferSpeed, Bar, Percentage, ETA
from libc.math cimport exp, log

@cython.boundscheck(False)
def do_histogram(dist, shape):
    print 'reading %s' % dist._v_name

    cdef np.ndarray[np.npy_double, ndim=1] X1 = np.zeros(shape, dtype=np.double)
    cdef np.ndarray[np.npy_double, ndim=1] X2 = np.zeros(shape, dtype=np.double)
    cdef np.ndarray[np.npy_double, ndim=1] X3 = np.zeros(shape, dtype=np.double)
    cdef np.ndarray[np.npy_double, ndim=1] X4 = np.zeros(shape, dtype=np.double)

    print 'computing ... '

    widgets = [FileTransferSpeed(), ' ', Bar(), ' ',
               Percentage(), ' ', ETA()]

    cdef np.uint64_t n
    cdef np.uint64_t x
    cdef np.npy_double W

    pbar = ProgressBar(widgets=widgets, maxval = dist.nrows)
    pbar.start()
    for row in dist:
        n = row[0]
        x = row[1]
        W = row[2]
        X1[n] += W * x 
        X2[n] += W * x ** 2
        X3[n] += W * x ** 3
        X4[n] += W * x ** 4

        pbar.update(row.nrow)

    return
