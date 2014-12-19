import scipy.optimize

def crossing_analysis(O, w_min, w_max, l):
    w = np.linspace(w_min, w_max, 500)
    w_, l_ = np.ix_(w, l)
    lines = plt.plot(w, O(w_, l_))
    for x, y in zip(lines, l):
        x.set_label('$n = %d$' % y)

    plt.xlim(w_min, w_max)
    plt.xlabel(r'$\omega$')
    plt.legend(loc = 0)

def cross(O, L1, L2):
    L1, L2 = sorted((L1, L2))
    w_min = scipy.optimize.fmin(lambda w: O(w, L1) / O(w, L2), 1.8)
    print(w_min)
    w_max = scipy.optimize.fmin(lambda w: -O(w, L1) / O(w, L2), 1.8)
    print(w_max)
    return scipy.optimize.bisect(lambda w: O(w, L1) / O(w, L2) - 1, w_min, w_max)

# crossings = array([ cross(l1,l2) for l1, l2 in zip(l, l[1:]) ])

# plot(est(crossings, l[1:]), 'x', mew=1)
