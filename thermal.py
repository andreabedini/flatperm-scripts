omega = lambda group: group._v_attrs['omega']

m = lambda O, i: O[:,i] / O[:,0]

u = lambda O: m(O,1)

c = lambda O: m(O,2) - m(O,1)**2

t = lambda O: m(O,3) - 3 * m(O,2) * m(O,1) + 2 * m(O,1)**3

