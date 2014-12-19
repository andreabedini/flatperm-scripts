import numpy as np
import scipy.optimize

def leastsq(x, y, *args, **kwargs):
    include_zero = kwargs.pop('include_zero', False)
    fit_range = kwargs.pop('fit_range', slice(None))

    x = x.astype(float)
    y = y.astype(float)

    linear = lambda p: p[0] + p[1] * x[fit_range] - y[fit_range]

    a, b = scipy.optimize.leastsq(linear, [1, 1])[0]

    print(('intercept {} slope {}'.format(a, b)))

    if 'axis' in kwargs:
        ax = kwargs.pop('axis')
    else:
        from matplotlib import pyplot
        ax = pyplot.gca()
        
    xe = np.array(ax.get_xbound())

    if include_zero:
        xe[0] = 0

    print(xe)
    print((a + b * xe))

    if 'label' in kwargs:
        kwargs['label'] = kwargs['label'].format(intercept = a, slope = b)

    line = ax.plot(xe, a + b * xe, **kwargs)
    return {'line': line[0], 'intercept': a, 'slope': b}
