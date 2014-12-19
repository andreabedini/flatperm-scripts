import numpy as np

def convergent(n, x):
    i = n[::4]
    est = np.log2( (x[i] - x[i/2]) / (x[i/2] - x[i/4]) )
    return i, est
