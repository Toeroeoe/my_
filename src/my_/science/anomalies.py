import numpy as np
import pandas as pd

def standard_index(array: np.ndarray, 
                    variable: str = 'var',
                    unit: str = 'unit',
                    year_start: int = 1995,
                    year_end: int = 2018,
                    resolution: str = '8D', 
                    distribution: str = 'gamma',
                    rolling: bool = True,
                    window: str = '360D', 
                    agg_method: str = 'sum',
                    plot_distributions: bool = False,
                    plot_sxi_ts: bool = False,
                    plot_hist_bins: int = 30,
                    plot_lw: float = 2.0) -> np.ndarray:

    from my_figures.single import square, square_top_cax
    from my_figures.save import save_png
    from my_plot.basic import hist, plot
    from my_series.time import index
    from my_plot.init_ax import init_dist, init_ts_2
    from my_math.stats import distribution_fit, distribution_pdf, distribution_cdf
    from my_plot.legend import color_legend

    if isinstance(array, list): array = array[0]

    time_index              = index(year_start, year_end, resolution)

    time_index_valid        = time_index.loc[time_index[0] + pd.Timedelta(window):]

    series                  = pd.Series(array, index = time_index)

    # aggregate series too in next line??

    series_roll             = series.rolling(window).agg(agg_method) if rolling else series

    series_roll_valid       = series_roll.loc[time_index[0] + pd.Timedelta(window):]

    dummy_out               = pd.Series([np.nan] * len(series), index = time_index)

    if (distribution == 'gamma') & (np.any(series_roll_valid < 0) | np.all(series_roll_valid == 0)): return dummy_out

    if np.all(np.isnan(series_roll_valid)): return dummy_out


    if distribution == 'gaussian_kde':

        from my_math.stats import gauss_kde_pdf, gauss_kde_cdf

        pdf_xs, pdf_ys          = gauss_kde_pdf(series_roll_valid)

        cdf_xs, cdf_ys          = gauss_kde_cdf(series_roll_valid)

    else:

        parameter               = distribution_fit(series_roll_valid, distribution = distribution)

        pdf_xs, pdf_ys          = distribution_pdf(distribution = distribution,
                                                parameter = parameter)
    
        cdf_xs, cdf_ys          = distribution_cdf(distribution = distribution,
                                                parameter = parameter)
    
    pdf_normal_xs, pdf_normal_ys = distribution_pdf()

    cdf_normal_xs, cdf_normal_ys = distribution_cdf()

    series_roll_cdf         = np.interp(series_roll_valid, cdf_xs, cdf_ys)

    series_roll_sxi         = np.interp(series_roll_cdf, cdf_normal_ys, cdf_normal_xs)

    if plot_distributions: 
        
        fig, ax = square(4, 4)
        init_dist(ax, pdf_xs, pdf_ys, xlabel = f'{variable} [{unit} {window}' + r'$\mathdefault{^{-1}}$]', ylabel = 'Probability density')
        plot(ax, xs = pdf_xs, ys = pdf_ys, lw = plot_lw, zorder = 2)
        hist(ax, series_roll, bins = plot_hist_bins, zorder = 1)
        save_png(fig, f'PDF_{variable}_{distribution}_{window}_{agg_method}.png')

        fig, ax = square(4, 4)
        init_dist(ax, cdf_xs, cdf_ys, xlabel = f'{variable} [{unit} {window}' + r'$\mathdefault{^{-1}}$]', ylabel = 'Cummulative probability density')
        plot(ax, xs = cdf_xs, ys = cdf_ys, lw = plot_lw, zorder = 2)
        save_png(fig, f'CDF_{variable}_{distribution}_{window}_{agg_method}.png')
    
        fig, ax = square(4, 4)
        init_dist(ax, pdf_normal_xs, pdf_normal_ys, xlabel = 'SXI', ylabel = 'Probability density')
        plot(ax, xs = pdf_normal_xs, ys = pdf_normal_ys, lw = plot_lw, zorder = 2)
        save_png(fig, 'pdf_norm.png')    

        fig, ax = square(4, 4)
        init_dist(ax, cdf_normal_xs, cdf_normal_ys, xlabel = 'SXI', ylabel = 'Cummulative probability density')
        plot(ax, xs = cdf_normal_xs, ys = cdf_normal_ys, lw = plot_lw, zorder = 2)
        save_png(fig, 'cdf_norm.png')

    if plot_sxi_ts:
        
        fig, ax, cax = square_top_cax(fy = 4)
        init_ts_2(ax, time_index, np.concatenate([array, series_roll_sxi]), xlabel = 'Time', ylabel = f'SXI [-] / {variable} [{unit} {window}' + r'$\mathdefault{^{-1}}$]')
        plot(ax, xs = time_index, ys = array, colors = 'k', lw = plot_lw, zorder = 2)
        plot(ax, xs = time_index_valid, ys = series_roll_sxi, lw = plot_lw, colors = 'firebrick', zorder = 2)
        color_legend(cax, {variable: 0, 'SXI': 1}, ['k', 'firebrick'])        
        save_png(fig, f'SXI_{variable}_{distribution}_{window}_{agg_method}.png')


    return series_roll_sxi


if __name__ == '__main__':

    from my_files.netcdf import open_netcdf, variables_to_array

    path                    = '/p/scratch/cjibg31/jibg3105/data/COSMOREA6/8daily/'
    year_start              = 1995
    year_end                = 2018
    #variables               = ['GPP', 
    #                           'QFLX_EVAP_TOT', 
    #                           'QFLX_EVAP_VEG', 
    #                           'QFLX_EVAP_GRND', 
    #                           'RAIN',
    #                           'QOVER',
    #                           'ZWT',
    #                           'TWS']
    
    variables = ['PRECTmms']

    #variables_names         = ['GPP',
    #                            'ET', 
    #                            'Tr', 
    #                            'ET soil', 
    #                            'Rain',
    #                            'Runoff',
    #                            'ZWT',
    #                            'TWS']
    
    variables_names = ['Precipitation']

    #variables_transform     = [8 * 60 * 60 * 24,
    #                           8 * 60 * 60 * 24,
    #                           8 * 60 * 60 * 24,
    #                           8 * 60 * 60 * 24,
    #                           8 * 60 * 60 * 24,
    #                           8 * 60 * 60 * 24,
    #                           1,
    #                           1]

    variables_transform = [8*60*60*24]

    variables_units     = [r'$\mathdefault{mm}$']
    i_lat                   = 812
    i_lon                   = 712

    files                   = [f'{path}/{y}.nc' for y in range(year_start, year_end + 1)]

    data                    = open_netcdf(files)

    arrays                  = variables_to_array(data, variables)
    arrays_loc              = [a[:, i_lat, i_lon] * variables_transform[i] for i, a in enumerate(arrays)]
    

    for i, v in enumerate(variables_names):
        
        standard_index(arrays_loc[i], v,
                    unit = variables_units[i],
                    distribution = 'gamma',
                    year_start = year_start,
                    year_end = year_end,
                    plot_distributions = True, 
                    plot_sxi_ts = True,
                    window = '360D')