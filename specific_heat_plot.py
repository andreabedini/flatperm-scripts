from analisys import bestfit

def specific_heat(hf, **kwargs):
    I = slice(100, -1, 20)
    n = arange(hf.root.sW.shape[0])[I]
    p = hf.root.st_peak.cols.cpeak[I] / n
    plot(log(n), log(p), **kwargs)
    bestfit.leastsq(log(n), log(p), label = 'slope {slope:.3f}')
    legend(loc = 0)
    xlabel(r'$\log\ n$')
    ylabel(r'$\log\ c_n^p$')

def specific_heat_errorbars(hfs, **kwargs):
    I = slice(100, -1, 20)
    n = arange(hfs[0].root.sW.shape[0])[I]
    p = array([ hf.root.st_peak.cols.cpeak[I] / n for hf in hfs ])
    yerr = p.std(0) / p.mean(0) ## log scale
    kwargs.update(linestyle = '')
    errorbar(log(n), log(p.mean(0)), yerr = yerr, label = '', **kwargs)
    bestfit.leastsq(log(n), log(p.mean(0)), label = 'slope {slope:.3f}')
    legend(loc = 0)
    xlabel(r'$\log\ n$')
    ylabel(r'$\log\ c_n^p$')
