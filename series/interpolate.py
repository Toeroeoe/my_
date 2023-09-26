
def resample(df, offset_str, method: str = 'mean'):

    import pandas as pd

    method_pd                   = getattr(pd.DataFrame, method)

    df_resampler                = df.resample(offset_str)

    df_resampled                = df_resampler.agg(method_pd, skipna = False)

    return df_resampled


def resample_yearly(df, offset_str: str = 'D', method: str = 'mean'):

    import pandas as pd

    method_pd                   = getattr(pd.DataFrame, method)

    df_y_groups                 = df.groupby(df.index.year, group_keys=False)
    df_y_resampler              = df_y_groups.resample(offset_str)

    df_resampled                = df_y_resampler.agg(method_pd, skipna=False)

    return df_resampled



def reindex(df, timeseries, method =  None):

    df_new_time                 = df.reindex(timeseries, method = method)

    return df_new_time

    