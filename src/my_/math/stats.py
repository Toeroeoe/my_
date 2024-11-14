
import pandas as pd
import numpy as np
import scipy.stats as stats
    
def mean(array, axis: int | tuple | None = None, std_error = False):

    array_mean = np.nanmean(array, axis = axis)

    return array_mean


def std_error_mean(array, axis: int | tuple | None = None):

    array_std = np.nanstd(array, axis = axis)

    array_n = np.count_nonzero(~np.isnan(array), axis = axis)

    array_std_error_mean= array_std / np.sqrt(array_n)

    return array_std_error_mean


def variance(array, axis: int | tuple | None = None):

    array_var = np.nanvar(array, axis = axis)

    return array_var


def std_deviation(array, axis: int | tuple | None = None):

    array_std = np.nanstd(array, axis = axis)

    return array_std


def std_error_variance(array, axis: int | tuple | None = None):

    array_var = np.nanvar(array, axis = axis)

    array_n = np.count_nonzero(~np.isnan(array), axis = axis)

    array_std_error_var = np.sqrt(2 / (array_n - 1)) * array_var

    return array_std_error_var


def skewness(array, axis: int | None = None, nan_policy = 'omit'):

    from scipy.stats import skew

    array_skew = skew(array, axis, nan_policy = nan_policy)

    return array_skew


def std_error_skewness(array, axis: int | tuple | None = None):

    array_n = np.count_nonzero(~np.isnan(array), axis = axis)

    array_std_error_sk = np.sqrt((6 * array_n * (array_n - 1)) / 
                                  ((array_n - 2) * (array_n + 1) * (array_n + 3)))

    return array_std_error_sk


def kurtosis(array, axis: int | None = None, nan_policy = 'omit'):

    from scipy.stats import kurtosis

    array_kurtosis = kurtosis(array, axis, nan_policy = nan_policy)

    return array_kurtosis


def std_error_kurtosis(array, axis: int | tuple | None = None):

    array_n = np.count_nonzero(~np.isnan(array), axis = axis)

    array_std_error_sk = std_error_skewness(array, axis = axis)
    
    array_std_error_krt = 2 * array_std_error_sk * np.sqrt((array_n**2 - 1) / ((array_n - 3) * (array_n + 5)))

    return array_std_error_krt


def confidence_bands(x: np.ndarray,
                     y: np.ndarray,
                     level: float = 0.95,
                     n_pts: None | int = None):
    
    if n_pts is None: n_pts = len(x)

    mask = ~np.isnan(x) & ~np.isnan(y)

    x_clean, y_clean = x[mask], y[mask]

    lr = stats.linregress(x_clean, y_clean)

    trend = lr.intercept + x_clean * lr.slope

    tinv = lambda q, nu: abs(stats.t.ppf(q/2, nu))
    
    ts = tinv(1 - level, len(x_clean) - 2)
    
    yerr = 

    slopes = np.linspace(lr.slope + ts * lr.stderr, 
                         lr.slope - ts * lr.stderr,
                         n_pts)
    
    intercepts = np.linspace(lr.intercept + ts * lr.intercept_stderr, 
                             lr.intercept - ts * lr.intercept_stderr, 
                             n_pts)
    
    lines = np.empty([n_pts, len(x_clean)])
    
    x_fill = np.sort(x_clean)

    for i in range(len(slopes)):

        lines[i,:] = x_fill * slopes[i] + intercepts[i]

    lower = np.min(lines, axis = 0)
    upper = np.max(lines, axis = 0)

    return x_clean, trend, lower, upper