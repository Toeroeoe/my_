
import pandas as pd
import numpy as np
    
def mean(array, axis: int | tuple | None = None, std_error = False):

    import numpy as np

    array_mean          = np.nanmean(array, axis = axis)

    return array_mean


def std_error_mean(array, axis: int | tuple | None = None):

    import numpy as np

    array_std           = np.nanstd(array, axis = axis)

    array_n             = np.count_nonzero(~np.isnan(array), axis = axis)

    array_std_error_mean= array_std / np.sqrt(array_n)

    return array_std_error_mean


def variance(array, axis: int | tuple | None = None):

    import numpy as np

    array_var           = np.nanvar(array, axis = axis)

    return array_var


def std_deviation(array, axis: int | tuple | None = None):

    import numpy as np

    array_std           = np.nanstd(array, axis = axis)

    return array_std


def std_error_variance(array, axis: int | tuple | None = None):

    import numpy as np

    array_var           = np.nanvar(array, axis = axis)

    array_n             = np.count_nonzero(~np.isnan(array), axis = axis)

    array_std_error_var = np.sqrt(2 / (array_n - 1)) * array_var

    return array_std_error_var


def skewness(array, axis: int | None = None, nan_policy = 'omit'):

    from scipy.stats import skew

    array_skew          = skew(array, axis, nan_policy = nan_policy)

    return array_skew


def std_error_skewness(array, axis: int | tuple | None = None):

    import numpy as np

    array_n             = np.count_nonzero(~np.isnan(array), axis = axis)

    array_std_error_sk  = np.sqrt((6 * array_n * (array_n - 1)) / 
                                  ((array_n - 2) * (array_n + 1) * (array_n + 3)))

    return array_std_error_sk


def kurtosis(array, axis: int | None = None, nan_policy = 'omit'):

    from scipy.stats import kurtosis

    array_kurtosis      = kurtosis(array, axis, nan_policy = nan_policy)

    return array_kurtosis


def std_error_kurtosis(array, axis: int | tuple | None = None):

    import numpy as np

    array_n             = np.count_nonzero(~np.isnan(array), axis = axis)

    array_std_error_sk  = std_error_skewness(array, axis = axis)
    
    array_std_error_krt = 2 * array_std_error_sk * np.sqrt((array_n**2 - 1) / ((array_n - 3) * (array_n + 5)))

    return array_std_error_krt


def rmse(obs, sim, decimals=2):

    """
    Root mean square error 
    Use this to compare model to observation series
    """
    
    import numpy as np
    
    from my_.series.convert import tab_to_array

    obs                             = tab_to_array(obs)
    sim                             = tab_to_array(sim)
    
    error                           = sim - obs

    if np.all(np.isnan(error)): return np.nan

    squared_error                   = error**2

    sum_squared_error               = np.nansum(squared_error)

    n                               = np.count_nonzero(~np.isnan(error))

    mean_squared_error              = sum_squared_error / n

    rmse                            = mean_squared_error**0.5

    rmse_rounded                    = np.around(rmse, decimals)
    
    return rmse_rounded


def gauss_kde_pdf(data: pd.DataFrame | pd.Series | np.ndarray , 
                    n: int = 1000, 
                    return_dict: bool = False):
    
    import pandas as pd
    import numpy as np
    from scipy.stats import gaussian_kde

    if isinstance(data, pd.DataFrame): data = data.values
    if isinstance(data, pd.Series): data = data.values

    data_clean                      = data[~np.isnan(data)]

    mins                            = np.min(data_clean)

    maxs                            = np.max(data_clean)

    xs                              = np.linspace(mins, maxs, n)

    kde_sp                          = gaussian_kde(data_clean)

    ys                              = kde_sp.pdf(xs)

    if return_dict:     
        return pd.DataFrame({'xs': xs, 'ys': ys})
    else:
        return xs, ys


def gauss_kde_cdf(data, n = 1000):

    import pandas as pd
    import numpy as np
    from scipy.stats import gaussian_kde
    from scipy.special import ndtr

    if isinstance(data, pd.DataFrame): data = data.values
    if isinstance(data, pd.Series): data = data.values


    data_clean                      = data[~np.isnan(data)]

    mins                            = np.min(data_clean)

    maxs                            = np.max(data_clean)

    xs                              = np.linspace(mins, maxs, n)

    kde_sp                          = gaussian_kde(data_clean)

    ys                              = np.array([ndtr(np.ravel(x - kde_sp.dataset) / kde_sp.factor).mean() for x in xs])

    return xs, ys


def pbias(obs, sim, decimals: int = 2):

    import numpy as np

    from my_.series.convert import tab_to_array

    obs                             = tab_to_array(obs)
    sim                             = tab_to_array(sim)

    bias                            = sim - obs

    if np.all(np.isnan(bias)): return np.nan

    sum_bias                        = np.nansum(bias)

    sum_obs                         = np.nansum(obs)

    rel_bias                        = sum_bias / sum_obs
    
    percent_bias                    = rel_bias * 100

    percent_bias_rounded            = np.around(percent_bias, decimals)

    return percent_bias_rounded


def r(obs, sim, decimals: int = 2):

    import numpy as np
    from scipy.stats.stats import pearsonr

    from my_.series.convert import tab_to_array

    obs                             = tab_to_array(obs)
    sim                             = tab_to_array(sim)

    mask                            = ~np.isnan(obs) & ~np.isnan(sim)
    
    if np.count_nonzero(mask) <= 5: return np.nan

    obs_masked                      = obs[mask]
    sim_masked                      = sim[mask]

    r, p                            = pearsonr(obs_masked, sim_masked)

    r_rounded, p_rounded            = np.around(r, decimals), np.around(p, decimals)

    return r_rounded


def distribution_fit(array, distribution: str = 'gamma'):

    import scipy.stats as stats

    if distribution == 'gaussian_kde': return array

    func_dist                       = getattr(stats, distribution)

    parameters                      = func_dist.fit(array)

    return parameters


def distribution_pdf(distribution: str = 'norm', parameter: int | list = [0, 1], n = 100000):

    import scipy.stats as stats
    import numpy as np

    func_dist                       = getattr(stats, distribution)

    mins                            = func_dist.ppf(1/n, *parameter)

    maxs                            = func_dist.ppf(1 - 1/n, *parameter)

    xs                              = np.linspace(mins, maxs, n)

    ys                              = func_dist.pdf(xs, *parameter)

    return xs, ys


def distribution_cdf(distribution: str = 'norm', parameter: int | list = [0, 1], n = 100000):

    import scipy.stats as stats
    import numpy as np

    func_dist                       = getattr(stats, distribution)


    mins                            = func_dist.ppf(1/n, *parameter)

    maxs                            = func_dist.ppf(1 - 1/n, *parameter)

    xs                              = np.linspace(mins, maxs, n)

    ys                              = func_dist.cdf(xs, *parameter)

    return xs, ys


def distribution_data(distribution: str = 'norm', parameter: dict | tuple = {}, n = 100000):

    #Baustelle

    import scipy.stats as stats
    import numpy as np

    func_dist                       = getattr(stats, distribution)

    data                            = func_dist.rvs(0, 1, n)    


