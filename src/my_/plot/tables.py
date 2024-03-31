
def single_site_model_benchmarks(name, df, variable: str, obs: str, df_static, sel_landcover):

    print('Calculate model benchmarks based on single sites and observations\n')

    import pandas as pd
    
    from my_series.group import select_multi_index, nona_level
    from my_series.aggregate import single_column_wise
    from my_math.stats import rmse, pbias, r
    from my_files.handy import save_df

    df_nona                     = nona_level(df, ['Variable', 'Station'])

    df_n                        = select_multi_index(df_nona, ['Variable', 'Landcover'],
                                                      keys = [variable, sel_landcover])
    
    df_groups                   = df_n.groupby(axis = 1, level = ['Station'], group_keys = False)

    df_rmse                     = df_groups.apply(single_column_wise, level = 'Source', key = obs, ffunc = rmse)
    df_pbias                    = df_groups.apply(single_column_wise, level = 'Source', key = obs, ffunc = pbias)
    df_r                        = df_groups.apply(single_column_wise, level = 'Source', key = obs, ffunc = r)

    names                       = df_static['name']
    lc                          = df_static['landcover']
    vars                        = [variable] * len(lc)

    df_count                    = df_n.count().droplevel(['Variable', 'Landcover']).unstack().T.reindex(names)
    
    df_lc_count                 = df_n.groupby(axis = 1, level = ['Source', 'Landcover']).count().sum().T

    new_cols                    = pd.MultiIndex.from_arrays([vars, lc, names])

    df_rmse_sort                = df_rmse.reindex(new_cols, axis = 1).T
    df_pbias_sort               = df_pbias.reindex(new_cols, axis = 1).T
    df_r_sort                   = df_r.reindex(new_cols, axis = 1).T

    save_df(df_rmse_sort, f'out/{name}/csv/stations_rmse_{variable}.csv')
    save_df(df_pbias_sort, f'out/{name}/csv/stations_pbias_{variable}.csv')
    save_df(df_r_sort, f'out/{name}/csv/stations_r_{variable}.csv')
    save_df(df_count, f'out/{name}/csv/stations_count_{variable}.csv')
    save_df(df_lc_count, f'out/{name}/csv/landcover_count_{variable}.csv')
    


def landcover_model_benchmarks(name, df, variable: str, obs: str, df_static, sel_landcover):

    print('Calculate model benchmarks based on landcover and observations\n')
    
    from my_series.group import select_multi_index, nona_level
    from my_series.aggregate import single_level_wise, count_nonzero, concat
    from my_math.stats import rmse, pbias, r
    from my_files.handy import save_df

    import pandas as pd

    df_nona                     = nona_level(df, ['Variable', 'Station'])

    df_n                        = select_multi_index(df_nona, ['Variable', 'Landcover'],
                                                      keys = [variable, sel_landcover])
    
    df_groups                   = df_n.groupby(axis = 1, level = ['Landcover'])

    df_groups_rmse              = df_groups.apply(single_level_wise, level = 'Source', key = obs, ffunc = rmse)
    df_groups_pbias             = df_groups.apply(single_level_wise, level = 'Source', key = obs, ffunc = pbias)
    df_groups_r                 = df_groups.apply(single_level_wise, level = 'Source', key = obs, ffunc = r)

    df_groups_count             = pd.DataFrame({'count': df_groups.apply(count_nonzero)})

    df_out                      = df_groups_pbias.join(df_groups_rmse).T.swaplevel(axis = 0)

    
    save_df(df_groups_count, f'out/{name}/csv/landcover_count_{variable}.csv')

    save_df(df_out, f'out/{name}/csv/landcover_rmse_pbias_{variable}.csv')


    
