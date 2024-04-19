
import pandas as pd
import xarray as xr
    
def resample(df: pd.DataFrame | pd.Series | xr.Dataset | xr.DataArray,
            offset_str: str, 
            method: str = 'mean',
            yearly_agg: bool = True,
            **kwargs) -> pd.DataFrame | pd.Series | xr.Dataset | xr.DataArray:
    
    print(f'\nResampling dataframe by {method} to {offset_str} time frequency...\n')

    if isinstance(df, xr.Dataset) | isinstance(df, xr.DataArray):

        func = getattr(xr.DataArray, method)
    
        index = 'time.year'
        
        offset_str = {'time': offset_str}

    elif isinstance(df, pd.DataFrame) | isinstance(df, pd.Series):

        func = getattr(pd.DataFrame, method)
    
        index = df.index.year

        if yearly_agg: df = df.groupby(index, group_keys = False)
    
    else: NotImplementedError

    df_resampler = df.resample(offset_str)

    df_resampled = func(df_resampler, **kwargs)

    return df_resampled


def resample_yearly(df, offset_str: str = 'D', method: str = 'mean'):

    ### Obsolete !!! (I think)

    import pandas as pd

    method_pd                   = getattr(pd.DataFrame, method)

    df_y_groups                 = df.groupby(df.index.year, group_keys = False)
    df_y_resampler              = df_y_groups.resample(offset_str)

    df_resampled                = df_y_resampler.agg(method_pd, skipna = False)

    return df_resampled



def reindex(df, timeseries, method =  None):

    df_new_time                 = df.reindex(timeseries, method = method)

    return df_new_time

    