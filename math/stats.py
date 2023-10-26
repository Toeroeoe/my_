
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
    import pandas as pd
    
    from my_.series.convert import tab_to_array

    obs                             = tab_to_array(obs)
    sim                             = tab_to_array(sim)
    
    error                           = obs - sim

    if np.all(np.isnan(error)): return np.nan

    squared_error                   = error**2

    mean_squared_error              = np.nanmean(squared_error)

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


def pbias(obs, sim, decimals: int = 2):

    import numpy as np

    from my_.series.convert import tab_to_array

    obs                             = tab_to_array(obs)
    sim                             = tab_to_array(sim)

    bias                            = sim - obs

    if np.all(np.isnan(bias)): return np.nan

    sum_bias                        = np.nansum(bias)

    sum_obs                         = np.nansum(np.abs(obs))

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