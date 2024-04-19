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
                   deseasonalize: bool = True,
                   window: str = '360D', 
                   agg_method: str = 'sum',
                   plot_distributions: bool = False,
                   plot_out_dir: str = 'png/',
                   plot_sxi_ts: bool = False,
                   plot_hist_bins: int = 30,
                   plot_lw: float = 2.0) -> np.ndarray:

    from my_.files.handy import create_dirs
    from my_.figures.single import square, square_top_cax
    from my_.figures.save import save_png
    from my_.plot.basic import hist, plot
    from my_.series.time import index
    from my_.plot.init_ax import init_dist, init_ts_2
    from my_.math.stats import distribution_fit, distribution_pdf, distribution_cdf
    from my_.plot.legend import color_legend

    create_dirs(plot_out_dir)

    if isinstance(array, list): array = array[0]

    time_index = index(year_start, 
                       year_end, 
                       resolution)

    valid_start = time_index.iloc[0] + pd.Timedelta(window)

    time_index_valid = time_index.loc[valid_start:]

    series = pd.Series(array,
                       index = time_index)

    if deseasonalize:

        series_mean_year = series.groupby(series.index.dayofyear, 
                                          group_keys = False) \
                                          .mean().values

        mean_year_sub = lambda x: x - series_mean_year

        series_deseasonalized = series.groupby(series.index.year, 
                                               group_keys = False) \
                                               .apply(mean_year_sub)

        series = series_deseasonalized

    series_roll = series.rolling(window).agg(agg_method) if rolling else series

    series_roll_valid = series_roll.loc[valid_start:]

    dummy_out = np.array([np.nan] * len(series)) 
                          #index = time_index)

    if ((distribution == 'gamma') and 
        (np.any(series_roll_valid < 0) or 
         np.all(series_roll_valid == 0))): return dummy_out

    if np.all(np.isnan(series_roll_valid)): return dummy_out

    if distribution == 'gaussian_kde':

        from my_.math.stats import gauss_kde_pdf, gauss_kde_cdf

        pdf_xs, pdf_ys = gauss_kde_pdf(series_roll_valid)

        cdf_xs, cdf_ys = gauss_kde_cdf(series_roll_valid)

    else:

        parameter = distribution_fit(series_roll_valid, 
                                     distribution = distribution)

        pdf_xs, pdf_ys = distribution_pdf(distribution = distribution,
                                          parameter = parameter)
    
        cdf_xs, cdf_ys = distribution_cdf(distribution = distribution,
                                          parameter = parameter)
    
    pdf_normal_xs, pdf_normal_ys = distribution_pdf()

    cdf_normal_xs, cdf_normal_ys = distribution_cdf()

    series_roll_cdf = np.interp(series_roll_valid, 
                                cdf_xs, 
                                cdf_ys)

    series_roll_sxi = np.interp(series_roll_cdf, 
                                cdf_normal_ys, 
                                cdf_normal_xs)

    str_deseasonalize = 'deseasonalized' if deseasonalize else ''

    file_out = '_'.join([f'{variable}',
                         f'{distribution}',
                         f'{window}',
                         f'{agg_method}',
                         f'{str_deseasonalize}'])

    if plot_distributions: 
        
        fig, ax = square(4, 4)
        init_dist(ax,pdf_xs, pdf_ys, xlabel = f'{window} {agg_method} {variable} [{unit}]', ylabel = 'Probability density')
        plot(ax, xs = pdf_xs, ys = pdf_ys, lw = plot_lw, zorder = 2)
        hist(ax, series_roll, bins = plot_hist_bins, zorder = 1)
        save_png(fig, f'{plot_out_dir}/PDF_{file_out}.png')

        fig, ax = square(4, 4)
        init_dist(ax, cdf_xs, cdf_ys, xlabel = f'{window} {agg_method} {variable} [{unit}]', ylabel = 'Cummulative probability density')
        plot(ax, xs = cdf_xs, ys = cdf_ys, lw = plot_lw, zorder = 2)
        save_png(fig, f'{plot_out_dir}/CDF_{file_out}.png')
    
        fig, ax = square(4, 4)
        init_dist(ax, pdf_normal_xs, pdf_normal_ys, xlabel = 'SXI', ylabel = 'Probability density')
        plot(ax, xs = pdf_normal_xs, ys = pdf_normal_ys, lw = plot_lw, zorder = 2)
        save_png(fig, f'{plot_out_dir}/pdf_norm.png')    

        fig, ax = square(4, 4)
        init_dist(ax, cdf_normal_xs, cdf_normal_ys, xlabel = 'SXI', ylabel = 'Cummulative probability density')
        plot(ax, xs = cdf_normal_xs, ys = cdf_normal_ys, lw = plot_lw, zorder = 2)
        save_png(fig, f'{plot_out_dir}/cdf_norm.png')

    if plot_sxi_ts:
        
        fig, ax, cax = square_top_cax(fy = 4)
        init_ts_2(ax, time_index, array, xlabel = 'Time', ylabel = f'{variable} [{unit}]')
        plot(ax, xs = time_index, ys = array, colors = 'k', lw = plot_lw, zorder = 2)
        color_legend(cax, {variable: 0}, ['k', 'firebrick'])        
        save_png(fig, f'{plot_out_dir}/TS_{file_out}.png')

        fig, ax, cax = square_top_cax(fy = 4)
        init_ts_2(ax, time_index, series_roll_sxi, xlabel = 'Time', ylabel = 'SXI [-]')
        plot(ax, xs = time_index_valid, ys = series_roll_sxi, lw = plot_lw, colors = 'firebrick', zorder = 2)
        color_legend(cax, {f'{variable} Standardized Index': 1}, ['k', 'firebrick'])        
        save_png(fig, f'{plot_out_dir}/SXI_{file_out}.png')

    return series_roll_sxi


if __name__ == '__main__':

    from my_.data import CLM5
    from my_.data.templates import gridded_data
    
    variables = ['GPP']
    year_start = 1995
    year_end = 2018
    i_lat = 812
    i_lon = 712
    dist = 'gaussian_kde'
    window = '360D'
    deseasonalize = True
    source = CLM5.BGC_EU3_8daily

    data = gridded_data(**source)
    arrays = data.get_values(variables,
                             y0 = year_start,
                             y1 = year_end)
      
    standard_index(arrays[variables[0]][:,i_lat, i_lon] * 60 * 60 * 24, 
                   variables[0],
                   unit = source['variable_units'][variables[0]],
                   distribution = dist,
                   deseasonalize = deseasonalize,
                   agg_method = 'sum',
                   year_start = year_start,
                   year_end = year_end,
                   plot_distributions = True, 
                   plot_sxi_ts = True,
                   window = window,)