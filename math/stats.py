
def mean(array, axes: int = 0):

    import numpy as np

    array_mean          = np.nanmean(array, axis = axes)

    return array_mean


def variance(array, axes):

    import numpy as np

    array_var           = np.nanvar(array, axis = axes)

    return array_var


def skew(array, axis: int, nan_policy = 'omit'):

    from scipy.stats import skew

    array_skew          = skew(array, axis, nan_policy = nan_policy)

    return array_skew


def kurtosis(array, axis: int, nan_policy = 'omit'):

    from scipy.stats import kurtosis

    array_kurtosis      = kurtosis(array, axis, nan_policy = nan_policy)

    return array_kurtosis


def rmse(obs, sim, decimals=2):

    """
    Root mean square error 
    Use this to compare model to observation series
    """
    
    import numpy as np
    
    # The error between observations and model
    error                           = obs - sim

    if all(np.isnan(error)): return np.nan
    
    # Squared error
    squared_error                   = error**2

    # Mean of the suqred error
    mean_squared_error              = np.nanmean(squared_error)

    # Root of the mean of the quared error
    rmse                            = mean_squared_error**0.5

    rmse_rounded                    = np.around(rmse, decimals)
    
    return rmse_rounded


def gauss_kde_pdf(data, n = 100):
    
    import pandas as pd
    import numpy as np
    from scipy.stats import gaussian_kde

    if isinstance(data, pd.DataFrame): data = data.values

    data_clean                      = data[~np.isnan(data)]

    xs                              = np.linspace(np.min(data_clean), np.max(data_clean), n)
    kde_sp                          = gaussian_kde(data_clean)
    ys                              = kde_sp.pdf(xs)

    return pd.DataFrame({'xs': xs, 'ys': ys})


def percent_bias(obs, sim, decimals: int = 2):

    import pandas as pd
    import numpy as np

    if isinstance(obs, pd.DataFrame): obs = obs.values

    error                           = obs - sim

    sum_error                       = np.nansum(error)

    sum_obs                         = np.nansum(obs)

    rel_error                       = sum_error / sum_obs

    percent_bias                    = rel_error * 100

    percent_bias_rounded            = np.around(percent_bias, decimals)

    return percent_bias_rounded