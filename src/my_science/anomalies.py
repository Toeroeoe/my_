
import numpy as np
import pandas as pd

from my_files.netcdf import open_netcdf, netcdf_variable_to_array

def standard_index(array: np.ndarray, 
                    variable: str = 'var',
                    year_start: int = 1995, 
                    year_end: int = 2018,
                    resolution: str = '8D', 
                    distribution: str = 'gamma',
                    rolling: bool = True,
                    window: str = '180D', 
                    agg_method: str = 'sum',
                    plot_distributions: bool = False,
                    plot_sxi_ts: bool = False) -> np.ndarray:

    from my_figures.single import square
    from my_figures.save import save_png
    from my_plot.basic import hist, plot
    from my_series.time import index
    from my_plot.init_ax import init_dist, init_ts_2
    from my_math.stats import distribution_fit, distribution_pdf, distribution_cdf

    time_index              = index(year_start, year_end, resolution)

    series                  = pd.Series(array, index = time_index)

    series_roll             = series.rolling(window).agg(agg_method) if rolling else series

    parameter               = distribution_fit(series_roll, distribution = distribution)

    pdf_xs, pdf_ys          = distribution_pdf(distribution = distribution,
                                               parameter = parameter)
    
    cdf_xs, cdf_ys          = distribution_cdf(distribution = distribution,
                                               parameter = parameter)
    
    pdf_normal_xs, pdf_normal_ys = distribution_pdf()

    cdf_normal_xs, cdf_normal_ys = distribution_cdf()

    series_roll_cdf         = np.interp(series_roll, cdf_xs, cdf_ys)

    series_roll_sxi         = np.interp(series_roll_cdf, cdf_normal_ys, cdf_normal_xs)

    if plot_distributions: 
        
        fig, ax = square()
        init_dist(ax, pdf_xs, pdf_ys)
        plot(ax, xs = pdf_xs, ys = pdf_ys, lw = 2, zorder = 2)
        hist(ax, series_roll, bins = 30, zorder = 1)
        save_png(fig, 'pdf.png')

        fig, ax = square()
        init_dist(ax, cdf_xs, cdf_ys)
        plot(ax, xs = cdf_xs, ys = cdf_ys, lw = 2, zorder = 2)
        save_png(fig, 'cdf.png')
    
        fig, ax = square()
        init_dist(ax, pdf_normal_xs, pdf_normal_ys)
        plot(ax, xs = pdf_normal_xs, ys = pdf_normal_ys, lw = 2, zorder = 2)
        save_png(fig, 'pdf_norm.png')    

        fig, ax = square()
        init_dist(ax, cdf_normal_xs, cdf_normal_ys)
        plot(ax, xs = cdf_normal_xs, ys = cdf_normal_ys, lw = 2, zorder = 2)
        save_png(fig, 'cdf_norm.png')

    if plot_sxi_ts:
        
        fig, ax = square(fy= 4)
        init_ts_2(ax, time_index, [array, series_roll_sxi])
        plot(ax, xs = time_index, ys = array, colors = 'k', lw = 2, zorder = 2)
        plot(ax, xs = time_index, ys = series_roll_sxi, lw = 2, colors = 'firebrick', zorder = 2)
        save_png(fig, f'SXI_{variable}_{distribution}_{window}_{agg_method}.png')

    return series_roll_sxi

if __name__ == '__main__':

    # Does not work as callable script yet
    # Baustelle

    path                    = '/p/scratch/cjibg31/jibg3105/data/COSMOREA6/8daily/'
    year_start              = 1995
    year_end                = 1996
    variable                = 'PRECTmms'
    #coordinates             = 

    files                   = [f'{path}/{y}.nc' for y in range(year_start, year_end + 1)]

    data                    = open_netcdf(files)

    array                   = netcdf_variable_to_array(data, variable)
    
    standard_index(path, 'PRECTmms')