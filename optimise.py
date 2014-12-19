import scipy.optimize

def fmin(*a, **d):
    d.update(full_output = 1)
    d.update(disp = False)
    (x,), y, _, _, _, = scipy.optimize.fmin(*a, **d)
    return (x, y)

def fmax(*a, **d):
    d.update(full_output = 1)
    d.update(disp = False)
    (x,), y, _, _, _, = scipy.optimize.fmin(*a, **d)
    return (x, y)

