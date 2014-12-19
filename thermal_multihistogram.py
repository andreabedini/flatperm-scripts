import pylab as pl
import numpy as np

def resampled_hist(hist, wo, wn):
    n = np.indices(hist.shape)[0]
    # print 'n shape', n.shape
    # print 'hist shape', hist.shape
    # print 'wo shape', wo.shape
    if not np.isscalar(wn):
        wn = np.atleast_1d(wn)[...,None,None]
    return hist * (wn / wo) ** n

def resampled_multihist(hist, wo, wn, sigma = 0.001):
    A = resampled_hist(hist, wo, wn)
    if not np.isscalar(wn):
        wn = np.atleast_1d(wn)[...,None,None]
    W = np.exp(-(wn - wo)**2 / sigma)
    return np.sum(A * W, -1) / np.sum(A * W)

class combine:
    def __init__(self, hists, wo, sigma = 0.001):
        self.wo = wo
        self.sigma = sigma
        
        A = np.log(hists.T / hists.sum(1)).T
        hists[A < -50] = 0
        n = np.indices(hists.shape)[-1]
        self.log_hists = np.log(hists) - n * np.log(wo)
        self.log_hists = self.log_hists - self.log_hists.max()
        
    def dist(self, wn):
        W = np.exp(-(wn - self.wo)**2 / self.sigma)
        n = np.indices(self.log_hists.shape)[-1]
        log_temp = self.log_hists + n * np.log(wn)
        log_temp = log_temp - log_temp.max()

        temp = np.sum(W * np.exp(log_temp), axis = 0) / np.sum(W, axis = 0)
        return temp / temp.sum()

    def moment(self, moment, wn):
        dist = self.dist(wn)
        n = np.indices(dist.shape)[0]
        return np.sum(dist * n ** moment)

    def u(self, w):
        return self.moment(1, w)

    def c(self, w):
        return self.moment(2, w) - self.moment(1, w)**2

    def t(self, w):
        return self.moment(3, w) - 3 * self.moment(2, w) * self.moment(1, w) + 2 * self.moment(1, w)**3
