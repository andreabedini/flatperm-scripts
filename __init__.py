from . import flatperm

from scipy import interpolate

def smooth(n, x):
    return interpolate.splev(n, interpolate.splrep(n, x, s=1))
