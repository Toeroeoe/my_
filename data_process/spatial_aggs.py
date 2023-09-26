

def spatial_moments(name_case: str, sources = [], variables = [], year_start: int = 1995, year_end: int = 2018,
                    moments = ['nanmean', 'nanvar', 'skew', 'kurtosis']):

    print(f'\nIterate over gridded source data:\n{*sources,}\n')

    from my_.resources.sources import query_variables, available_variables
    from my_.files.handy import yearly_or_monthly_files, save_df
    from my_.files.netcdf import open_netcdf, netcdf_variables_to_array
    from my_.resources.units import transform

    from my_.gridded.spatial import func


    for src in sources:
     
        path                    = query_variables(src, 'path')
        freq_files              = query_variables(src, 'freq_files')
        time_step               = query_variables(src, 'time_step')
        leapday                 = query_variables(src, 'leap_day')
        grid                    = query_variables(src, 'grid')

        vars_avail, vars_src    = available_variables(src, variables)

        files                   = yearly_or_monthly_files(freq_files, path, year_start, year_end)

        print('Load data...\n')
        data                    = open_netcdf(files)
        arrays_list             = netcdf_variables_to_array(data, variables = vars_src)

        #columns                 = 

        for i_var, var in enumerate(vars_avail):

            array               = arrays_list[i_var]

            array_ux            = transform(array, src, var)

            for moment in moments:
                
                array_mom       = func(array_ux, moment)

                print(array_mom)





spatial_moments('cool', sources = ['CLM5-EU3'], variables = ['ET'])




