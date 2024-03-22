
def check_file_exists(str_file):

    from glob import glob

    if len(glob(str_file)) > 0:
        print(f'\nOutput file exists. Return.\n')
        return True
    
    else:
        print(f'\nOutput file does not exist. It will be created now...\n')
        return False


def yearly_files(path, y0: int = 1995, y1: int = 2018):

    files                   = [f"{path}/{str(y)}.nc" for y in range(y0, y1+1)]

    return files


def monthly_files(path, y0: int = 1995, y1: int = 2018):

    files                   = [f"{path}/{str(y)}-{str(m).zfill(2)}.nc" for y in range(y0, y1+1) for m in range(1,13)]

    return files


def yearly_or_monthly_files(freq_files, path, y0, y1):

    if freq_files == 'monthly':

        files               = monthly_files(path, y0, y1)

    elif freq_files == 'yearly':

        files               = yearly_files(path, y0, y1)

    return files


def save_df(df, name: str, format: str = 'csv'):

        if format == 'csv':
            
            df.to_csv(name)
        
        elif format == 'parquet':
            
            df.to_parquet(name)


def open_csv_or_parquet(file: str, csv_args = {'index_col': 0}, parquet_args = {}):

    from my_files.csv import open_csv
    from my_files.parquet import open_parquet

    ending                      = file.split('.')[-1]
    
    open_method                 = open_csv if ending == 'csv' else open_parquet

    args                        = csv_args if ending == 'csv' else parquet_args

    df                          = open_method(file, args)

    return df


def read_resample_save(case_name: str, files: list, origin: str, suffixes: list = [], file_format: str = 'parquet',
                        join: str = 'outer', offset_str: str = 'D', interp_method: str = 'mean'):

    from glob import glob
    from my_series.interpolate import resample_yearly
    from my_series.aggregate import concat
    from my_resources.sources import variables
    from my_series.group import layer_level_to_int

    
    file_out                    = f'out/{case_name}/{file_format}/Resampled_{origin}.{file_format}'

    list_dfs                    = []

    if glob(file_out): print('Resampled file found\n'); return open_csv_or_parquet(file_out)


    print('Resampling...\n')

    for i_f, f in enumerate(files):

        if len(suffixes) > 0:

            suffix              = f'_{suffixes[i_f]}'
        
        else: suffix = ''

        df                  = open_csv_or_parquet(f).add_suffix(suffix)

        src                 = df.columns.get_level_values('Source').unique()[0]

        if 'var_layer' in variables[src]:

            df_int          = layer_level_to_int(df)

            df_groups       = df_int.groupby(axis = 1, level = ['Source', 'Variable', 'Landcover', 'Station'])

            df              = df_groups.apply(aggregate_layer)

        list_dfs.append(df)
    
    df                      = concat(list_dfs, join = join, axis = 1)

    df_resampled            = resample_yearly(df, offset_str, method = interp_method)

    save_df(df_resampled, file_out, file_format)

    return df_resampled


def aggregate_layer(df):

    from my_resources.sources import query_variables

    from my_series.group import select_multi_index

    from user_in.options_analyses import selected_landcover


    src                     = df.columns.get_level_values('Source').unique()[0]

    var                     = df.columns.get_level_values('Variable').unique()[0]

    lc                      = df.columns.get_level_values('Landcover').unique()[0]

    if lc not in selected_landcover: return df.agg('mean', axis = 1)

    type_layer              = query_variables(src, 'var_layer')[var]

    method_agg              = query_variables(src, 'method_layer_agg')[type_layer]

    if type_layer == 'PFT':

        selection           = query_variables(src, f'sel_agg_layer_PFT')[lc]

        df_sel              = select_multi_index(df, 'Layer', [selection])

        df_agg              = df_sel.agg(method_agg, axis = 1)

    return df_agg

    
def create_dirs(dirs):

    from pathlib import Path

    for dir in dirs:
        
        Path(dir).mkdir(parents = True, exist_ok = True)


