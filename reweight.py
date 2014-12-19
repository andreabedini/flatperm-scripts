import numexpr as ne
import numpy as np
import tables

# m2 = lambda n: hf.root.table.readWhere('n == %d' % n, field = 'm2').astype(double)
# nn = lambda n: hf.root.table.readWhere('n == %d' % n, field = 'nn').astype(double)

# m2_energy = array([ m2(i).mean() for i in n ])
# nn_energy = array([ nn(i).mean() for i in n ])

def W(weights, user_ns):
    if weights:
        expr = ' * '.join('%f ** %s' % (v, k) for k,v in list(weights.items()))
        print(expr)
        w = ne.evaluate(expr, user_ns)
        print(('max correction %f' % w.max()))
        return w
    else:
        return None

def _hessian(expr, weights, user_ns):
    weights = W(weights, user_ns)
    avg = lambda O: np.average(O, weights = weights)
    O1, O2 = expr
    B = avg(O1)
    C = avg(O2)
    D = avg(O1*O1)
    E = avg(O1*O2)
    F = avg(O2*O2)
    a = D - B*B
    b = E - B*C
    c = F - C*C
    H = np.empty((2,2))
    H.flat = (a, b, b, c)
    return H

def reweighted_hessian(n, weights, hf):
    d = hf.root.table.readWhere('n == %d' % n)
    m2 = d['m2'].astype(np.double)
    nn = d['nn'].astype(np.double)

    m2 = m2.mean()
    nn = nn.mean()

    return _hessian([m2, nn], weights, {'m2': m2, 'nn': nn})
