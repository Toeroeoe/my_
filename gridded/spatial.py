

def func(array, method):

    import numpy as np

    if method == 'kurtosis':

        from scipy.stats import kurtosis

        func_method     = kurtosis
    
    elif method == 'skew':

        from scipy.stats import skew

        func_method     = skew

    else:

        func_method     = getattr(np, method)

    array_mean          = np.apply_over_axes(func_method, array, axes = (-1, -2))

    return array_mean

