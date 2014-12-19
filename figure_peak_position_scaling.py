import sys
from .tools import estimator3
import tables
import pylab as pl
import numpy as np

hf = tables.openFile(sys.argv[1])

x = 1.0 / hf.root.st_peak_scaling.cols.n[:]
y = hf.root.st_peak_scaling.cols.wpeak[:]

fig = pl.figure()

ax1 = fig.add_subplot(121)
ax1.plot(x, y, '.')
a, b = np.polyfit(x, y, 1)
ax1.plot(x, a * x + b, label='a = %f, b = %f' % (a,b))
ax1.legend(loc = 0)
ax1.set_xlabel('$n^{-1}$')
ax1.set_ylabel('peak position')

ax2 = fig.add_subplot(122)
ax2.plot(x[6:], estimator3(x, y))
ax2.set_xlabel('$n^{-1}$')
ax2.set_ylabel('exponent estimator')

fig.set_size_inches((15.5,   7.6))
fig.show()

if len(sys.argv) > 2:
    fig.savefig(sys.argv[2])
