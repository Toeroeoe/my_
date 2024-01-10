
def src_var_cells_df(name_case: str, sources = [], variables = [], file_format: str = 'csv',
                path_stations: str = 'user_in/csv/', file_stations: str = 'stations.csv',
                year_start: int = 1995, year_end: int = 2018):

    print(f'\nIterate over gridded source data:\n{*sources,}\n')

    from glob import glob
    from itertools import product

    from my_resources.sources import query_variables, query_grids, available_variables
    from my_files.handy import yearly_or_monthly_files, save_df
    from my_files.netcdf import open_netcdf, netcdf_variables_to_array
    from my_files.csv import open_csv
    from my_gridded.dimensions import grid_to_points
    from my_series.aggregate import concat
    from my_series.group import single_src_var_X_index
    from my_series.time import index
    from my_resources.units import transform
    from my_gridded.extract import grid_to_cell_df

    for src in sources:
        
        file_out                = f'out/{name_case}/{file_format}/Extracted_{src}.{file_format}'
        file_out_info           = f'out/{name_case}/csv/Cells_{src}.csv'

        if glob(file_out): print(f'Output file for {name_case} - {src} is already available.\n'); continue
        
        print(f'Output file for {src} is not available and will be created.\n')

        df_stations             = open_csv(f'{path_stations}/{file_stations}')
        df_cells_info           = df_stations.copy()

        names_stations          = df_stations['name']
        lat_stations            = df_stations['lat']
        lon_stations            = df_stations['lon']
        landcover               = df_stations['landcover']

        path                    = query_variables(src, 'path')
        freq_files              = query_variables(src, 'freq_files')
        time_step               = query_variables(src, 'time_step')
        leapday                 = query_variables(src, 'leap_day')
        grid                    = query_variables(src, 'grid')
        
        file_grid               = query_grids(grid, 'file')
        path_grid               = query_grids(grid, 'path')
        grid_lat                = query_grids(grid, 'var_lat')
        grid_lon                = query_grids(grid, 'var_lon')

        vars_avail, vars_src    = available_variables(src, variables)

        files                   = yearly_or_monthly_files(freq_files, path, year_start, year_end)

        print('Load data...\n')
        data                    = open_netcdf(files)
        arrays_list             = netcdf_variables_to_array(data, variables = vars_src, dtype = 'float32')

        data_geo                = open_netcdf(f'{path_grid}/{file_grid}')
        
        [lat2d, lon2d]          = netcdf_variables_to_array(data_geo, variables = [grid_lat, grid_lon], dtype ='float32')

        list_points             = grid_to_points(lat2d, lon2d)

        time                    = index(year_start, year_end, time_step, leapday)

        iterations              = product(range(len(names_stations)), range(len(vars_avail)))

        print('Iterate stations and variables...\n')
        list_ts                 = []

        for i_station, i_var in iterations:

            name_station        = names_stations[i_station]
            lc                  = landcover[i_station]
            lat_yx              = lat_stations[i_station]
            lon_yx              = lon_stations[i_station]
            var                 = vars_avail[i_var]
            array               = arrays_list[i_var]

            print(f"Extract site {names_stations[i_station]}, variable {vars_avail[i_var]}")
            print(f'Location: {lat_yx} latitude, {lon_yx} longitude.\n')

            column              = single_src_var_X_index(array, src, var, lc, name_station)
            
            idxs, coords, ts    = grid_to_cell_df(array = array,
                                                    list_points = list_points, 
                                                    shape = lat2d.shape, column = column,
                                                    lat_point = lat_yx, lon_point = lon_yx,
                                                    index = time)
            
            ts_ux               = transform(ts, src, var)

            list_ts.append(ts_ux)

            df_cells_info.loc[i_station,['lat_cell', 'lon_cell']] = coords
            df_cells_info.loc[i_station,['i_lat_cell', 'i_lon_cell']] = idxs
        
        df_out                  = concat(list_ts, sort = False)

        save_df(df_cells_info, file_out_info, 'csv')
        save_df(df_out, file_out, file_format)
    
    print('Done. Extracted cell data for all sources.\n')


def cell_static_info(name_case: str, sources = [], path_stations: str = 'user_in/csv/', file_stations: str = 'stations.csv'):

    """
    Take cell info dataframe from above and include 
    Additional static information on that cell
    """

    from glob import glob
    from itertools import product
    
    from my_resources.sources import query_static, query_grids
    from my_gridded.dimensions import grid_to_points
    from my_files.netcdf import open_netcdf, netcdf_variables_to_array
    from my_files.csv import open_csv
    from my_gridded.extract import closest_cell, cell
    from my_files.handy import save_df
    
    for src in sources:

        file_out                = f'out/{name_case}/csv/Static_data_{src}.csv'

        if glob(file_out): print(f'Static data output file for {src} is already available.\n'); continue

        df_stations             = open_csv(f'{path_stations}/{file_stations}')
        df_out                  = df_stations.copy()

        names_stations          = df_stations['name']
        lat_stations            = df_stations['lat']
        lon_stations            = df_stations['lon']

        path                    = query_static(src, 'path')
        file                    = query_static(src, 'file')
        grid                    = query_static(src, 'grid')
        variables               = query_static(src, 'static_vars')
        
        file_grid               = query_grids(grid, 'file')
        path_grid               = query_grids(grid, 'path')
        grid_lat                = query_grids(grid, 'var_lat')
        grid_lon                = query_grids(grid, 'var_lon')
        
        data_geo                = open_netcdf(f"{path_grid}/{file_grid}")
        
        [lat2d, lon2d]          = netcdf_variables_to_array(data_geo, variables = [grid_lat, grid_lon])

        data                    = open_netcdf(f'{path}/{file}')
        arrays_list             = netcdf_variables_to_array(data, variables = variables)

        # List of lat lon grid cell coordinates
        list_points             = grid_to_points(lat2d, lon2d)

        iterations              = product(range(len(names_stations)), range(len(variables)))

        for i_station, i_var in iterations:

            name_station        = names_stations[i_station]
            var                 = variables[i_var]
            lat_yx              = lat_stations[i_station]
            lon_yx              = lon_stations[i_station]
            array               = arrays_list[i_var]

            print(f'Extract site {name_station}, static data for {src} variable {var}')
            print(f'Location: {lat_yx} latitude, {lon_yx} longitude.\n')
            
            grid_shape          = lat2d.shape
            ndim                = array.ndim
            length              = array.shape[0]
            
            name_out            = f"{var}"
            names_out           = name_out if ndim == 2 else [f'{name_out}_{i}' for i in range(length)]

            [y, x], coords_cell = closest_cell([lat_yx, lon_yx], list_points, grid_shape)

            cell_station        = cell(array, y = y, x = x)

            df_out.loc[i_station, ['lat_cell', 'lon_cell']] = coords_cell
            df_out.loc[i_station, ['i_lat_cell', 'i_lon_cell']] = y, x
            df_out.loc[i_station, names_out] = cell_station

        save_df(df_out, file_out, 'csv')



if __name__ == '__main__':

    from argparse import ArgumentParser

    parser                      = ArgumentParser()

    parser.add_argument('--name', '-n', help='Name for your work', type=str)
    parser.add_argument('--sources', '-s', nargs='+', help='List of source names', type=str)
    parser.add_argument('--variables', '-v', nargs='+', help='List of variables', type=str)
    parser.add_argument('--path_stations', '-ps', help='Path to the stations file', default='user_in/csv/', type=str)
    parser.add_argument('--file_stations', '-fs', help='File name of the stations info', default='stations.csv', type=str)
    parser.add_argument('--file_format', '-ff', help='The file format ending of the output file', default='csv', type=str)
    parser.add_argument('--include_static', '-is', help='Include static information from source?', default=False, type=bool)
    parser.add_argument('--static_sources', '-ss', nargs='+', help='Static sources for extract', default='', type=str)
    parser.add_argument('--year_start', '-y0', help='Start year', type=int)
    parser.add_argument('--year_end', '-y1', help='Stop year', type=int)

    args                        = parser.parse_args()

    src_var_cells_df(name_case = args.name, sources = args.sources, variables = args.variables,
                    path_stations = args.path_stations, file_stations = args.file_stations,
                    file_format = args.file_format, year_start = args.year_start, year_end = args.year_end)
    
    
    if args.include_static:
        
        cell_static_info(args.name, args.static_sources, args.path_stations, args.file_stations)

