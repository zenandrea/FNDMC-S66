import numpy as np


def fun_lin( x, a, b ):
    return a + b * x


def fun_quad( x, a, b, c ):
    return a + b * x + c * x**2


def fun_cub( x, a, b, c, d ):
    return a + b * x + c * x**2 + d * x**3

def fun_quart( x, a, b, c, d, e ):
    return a + b * x + c * x**2 + d * x**3 + e * x**4


def fit_err( x, y, ye, fitfun=0, xmax=0, M=1000, Nx=100 ):
    from scipy.optimize import curve_fit
    import numpy as np
    if fitfun==0:
        def fitfun( x, a, b ):
            return a + b * x
    if xmax==0:
        xmax = x.max()+0.01
    # Generate M sets of random points 
    l = []
    for i in range(len(y)):
        l.append( np.random.normal(y[i],ye[i],M) )
    aa = np.vstack(l)
    #aa.shape
    # fit each set of points with a line set by Nx values in the range 0,xmax
    xlinspace = np.linspace( 0, xmax, Nx )
    l = []
    for i in range(M):
        #plt.plot(x,aa[:,i],'.')
        try:
            xdata = x
            ydata = aa[:,i]
            popt, pcov = curve_fit( fitfun, xdata=xdata, ydata=ydata, sigma=ye )
            funlinspace = fitfun( xlinspace, *popt )
            l.append(funlinspace)
            #plt.plot( xlinspace, funlinspace, '--')
        except:
            pass
    #plt.errorbar(x,y,ye,fmt='ok')
    fits = np.vstack(l)
    # compute mean and standard deviation of the fits
    m = fits.mean(axis=0)
    s = fits.std(axis=0,ddof=1)
    return xlinspace, m, s


def get_chi2_alpha_parfun( x, y, ye, xfit, yfit, p=1 ):
    from scipy.stats import chi2
    n = len(x)
    df = n-p-1
    sumz2 = 0.0
    for i, xi in enumerate(x):
        ii = np.argmin( (xfit-xi)**2 )
        di = y[i] - yfit[ii]
        zi = di / ye[i]
        sumz2 += zi**2
    alpha = 1 - chi2.cdf( sumz2, df=df )
    return sumz2, df, alpha
