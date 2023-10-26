

def src_var_insitu_df(name_case: str, sources = [], variables = [],
                        file_format: str = 'csv',
                        path_stations: str = 'user_in/csv/',
                        file_stations: str = 'stations.csv',
                        year_start: int = 1995, year_end: int = 2018):
    
    from glob import glob
    import pandas as pd

    from my_.resources.sources import query_variables

    for src in sources:
        
        file_out                = f'out/{name_case}/{file_format}/Insitu_{src}.{file_format}'

        if glob(file_out): print(f'Output file for {name_case} - {src} is already available.\n'); continue
        
        print(f'Output file for {src} is not available and will be created.\n')

        df_stations             = pd.read_csv(f'{path_stations}/{file_stations}')

        processing              = query_variables(src, 'processing')

        if processing == 'ONEFLUX':

            oneflux(name_case, df_stations, src, variables, qc_values = {'D': 0.8, 'H': 1.0},
                    file_out = file_out, file_format = file_format,
                    year_start = year_start, year_end = year_end)



        
    
def oneflux(name, df_stations, src: str, variables = [], resample_method = 'mean', 
            qc_flag: bool = True, qc_values: dict = {'D': 0.8, 'H': 1.0},
            file_format: str = 'csv', file_out: str = 'oneflux_out.csv',
            year_start: int = 1995, year_end: int = 2018):

    from my_.misc.list_dict_key import keys_same_value, translate_dict_values, filter_dict_keys
    from my_.resources.sources import query_variables, available_variables
    from my_.files.csv import open_csv 
    from my_.files.handy import save_df
    from my_.series.time import index, lowest_frequency, index_to_datetime
    from my_.series.group import  multi_columns
    from my_.series.interpolate import resample, reindex
    from my_.series.aggregate import mask_ge, mask_le, concat
    from my_.resources.units import transform_df
    
    

    path                        = query_variables(src, 'path')
    var_names                   = query_variables(src, 'var_names')
    time_steps                  = query_variables(src, 'var_time_step')
    qcs                         = query_variables(src, 'var_QC')
    csv_open_args               = query_variables(src, 'csv_open_args')
    date_formats                = query_variables(src, 'date_format')

    vars_avail, _               = available_variables(src, variables)

    names_stations              = df_stations['name'].values
    names_FLX_stations          = df_stations['FLX_name'].values
    landcover_stations          = df_stations['landcover'].values

    filtered_ts                 = filter_dict_keys(time_steps, vars_avail)
    grouped_ts                  = keys_same_value(filtered_ts)

    grouped_ts_src              = translate_dict_values(idict = grouped_ts, idict_translate = var_names)
    grouped_ts_qc               = translate_dict_values(idict = grouped_ts, idict_translate = qcs)

    list_ts                     = list(grouped_ts_src)
    lowest_freq_ts              = lowest_frequency(list_ts)

    time                        = index(y0 = year_start, y1 = year_end, t_res = lowest_freq_ts)

    list_dfs                    = []
   
    for i_station in range(len(names_stations)):

        name                    = names_stations[i_station]
        lc                      = landcover_stations[i_station]
        name_FLX                = names_FLX_stations[i_station]

        print(f'Extract site {name}, in-situ ONEFLUX data for {src}...\n')

        for ts in list_ts:
        
            file                = f'{path}/FLX_{name_FLX}*/FLX_*_FULLSET_{ts}*'
        
            ts_df               = open_csv(file, args = csv_open_args)

            ts_df_date          = index_to_datetime(ts_df, format = date_formats[ts])
        
            df_sel              = ts_df_date[grouped_ts_src[ts]]
            
            if qc_flag:

                qc_value        = qc_values[ts]
                    
                df_sel_qc       = ts_df_date[grouped_ts_qc[ts]]

                if ts == 'H':

                    df_sel      = mask_le(df_sel, df_sel_qc, qc_value)
                
                if ts == 'D':

                    df_sel      = mask_ge(df_sel, df_sel_qc, qc_value)

            df_sel_resampled    = resample(df_sel, lowest_freq_ts, resample_method)

            df_sel_reindexed    = reindex(df_sel_resampled, time)


            df_sel_transformed  = transform_df(df_sel_reindexed, src, grouped_ts[ts])
            
            new_cols            = multi_columns([[src], grouped_ts[ts], [lc], [name]], 
                                                names = ['Source', 'Variable', 'Landcover', 'Station'])

            df_sel_transformed.columns = new_cols

            list_dfs.append(df_sel_transformed)

    df_oneflux                  = concat(list_dfs)

    save_df(df_oneflux, file_out, file_format)


if __name__ == '__main__':

    from argparse import ArgumentParser

    parser                      = ArgumentParser()

    parser.add_argument('--name', '-n', help = 'Name for your work', type = str)
    parser.add_argument('--sources', '-s', nargs = '+', help = 'Names of source data', type = str)
    parser.add_argument('--variables', '-v', nargs = '+', help = 'List of variables', type = str)
    parser.add_argument('--file_format', '-ff', help = 'file format suffix for dataframe', type = str, default = 'csv')
    parser.add_argument('--path_stations', '-ps', help='Path of the station information file', type = str, default = 'user_in/csv/')
    parser.add_argument('--file_stations', '-fs', help='File name of the station information file', type = str, default = 'stations.csv')
    parser.add_argument('--year_start', '-y0', help='Start year', type = int, default = 1995)
    parser.add_argument('--year_end', '-y1', help='End year', type = int, default = 2018)

    args                        = parser.parse_args()

    src_var_insitu_df(name_case = args.name, sources = args.sources, variables = args.variables,
                        file_format = args.file_format, path_stations = args.path_stations,
                        file_stations = args.file_stations, year_start = args.year_start, year_end = args.year_end)