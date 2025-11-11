import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from mcmath.distributions import gauss_kde_pdf, gauss_kde_cdf
from mcmath.distributions import distribution_fit, distribution_pdf, distribution_cdf

def index_weight(sxi: np.ndarray,
                 weigh_mid: float,
                 weigh_steep: float) -> np.ndarray:

    # Weight SXI with logistic function
    # 10.1175/JHM-D-22-0115.1
    # Calculate logistic weight and set 1 values to np.nan
    
    w = np.where((~np.isnan(sxi) & (sxi < 0)),
                 1 / (1 + (weigh_mid / sxi)**weigh_steep),
                 np.nan)

    return w


def plot_dist(xs: np.ndarray | pd.Series, 
              ys: np.ndarray | pd.Series, 
              ys_hist: np.ndarray | pd.Series, 
              xlabel: str, 
              ylabel: str,
              plot_out_dir: str = 'png/') -> None:

    fig = plt.figure(figsize=(6.7, 6.7), dpi=300)
        
    ax = fig.add_subplot(1, 1, 1, frameon=False)

    ax.spines.right.set_visible(False)
    ax.spines.top.set_visible(False)
    ax.spines.bottom.set_visible(False)
    ax.spines.left.set_visible(False)

    ax.grid(which='major',
            color='dimgray',
            linestyle='--',
            visible=True,
            linewidth=0.9,
            alpha=0.45,
            zorder=0)
            
    ax.set_xlabel(xlabel, labelpad=10)
    ax.set_ylabel(ylabel, labelpad=10)

    ax.tick_params(axis='both', 
                   which='major', 
                   pad=10)
            
    ax.axhline(0, color='k', ls='--', lw = 2, alpha = 0.8, dashes = (4, 4), zorder = 0)
    ax.axvline(0, color='k', ls='--', lw = 2, alpha = 0.8, dashes = (4, 4), zorder = 0)

    ax.hist(ys_hist, bins=30, density=True, histtype='stepfilled', color='dimgray', alpha=0.8, zorder=1)
    ax.plot(xs, ys, color='k', lw = 2.0, zorder = 2)

    fig.savefig(f'{plot_out_dir}/pdf_hist.png', bbox_inches='tight', dpi=300)

def plot_sxi(time_index: pd.Series,
             time_valid: pd.Series,
             array: np.ndarray, 
             series_roll_sxi: np.ndarray, 
             ylabel: str,
             plot_out_dir: str = 'png/') -> None:

    fig = plt.figure(figsize=(6.7, 5), dpi=300)
    gs = GridSpec(ncols=1, nrows=2, figure=fig)
    ax1 = fig.add_subplot(gs[0, 0])
    ax2 = fig.add_subplot(gs[1, 0], sharex=ax1)

    for i, ax in enumerate([ax1, ax2]):

        ax.spines.right.set_visible(False)
        ax.spines.top.set_visible(False)
        ax.spines.bottom.set_visible(False)
        ax.spines.left.set_visible(False)

        ax.grid(which='major',
                color='dimgray',
                linestyle='--',
                visible=True,
                linewidth=0.9,
                alpha=0.45,
                zorder=0)
            
        ylabel = ylabel if i == 0 else 'Standardized Index [-]'

        ax.set_ylabel(ylabel=ylabel, labelpad=10)
        ax.set_xlabel('Time', labelpad=10)
        ax.tick_params(axis='both', which='major', pad=10)
        ax.axhline(0, 
                   color='k', 
                   ls='--', 
                   lw=2, 
                   alpha=0.8, 
                   dashes = (4, 4),
                   zorder = 0)
            
    ax1.plot(time_index, array, 'k', lw=2, zorder=2)
    ax2.plot(time_valid, series_roll_sxi, 'firebrick', lw=2, zorder=2)
    fig.savefig(f'{plot_out_dir}/array_sxi.png', bbox_inches='tight', dpi=300)


def standard_index(array: np.ndarray, 
                   time_index: pd.Series,
                   variable: str = 'var',
                   distribution: str = 'gamma',
                   rolling: bool = True,
                   reftime: tuple[pd.Timestamp, pd.Timestamp] | None = None,
                   deseasonalize: bool = True,
                   window: str = '365D', 
                   agg_method: str = 'sum',
                   plot_distributions: bool = False,
                   unit: None | str = None,
                   plot_out_dir: str = 'png/',
                   plot_sxi_ts: bool = False) -> np.ndarray:

    if isinstance(array, list): array = array[0]

    if (distribution == 'gamma') and deseasonalize: 
                       
        print('\nDeseasonalize and gamma distribution')
        print('are not compatible...\n')

        raise NotImplementedError

    valid_start = time_index.iloc[0] + pd.Timedelta(window)

    series = pd.Series(array,
                       index=time_index)
    
    series.index = pd.DatetimeIndex(series.index)

    if deseasonalize:

        series_mean_year = series.groupby(series.index.dayofyear, 
                                          group_keys=False) \
                                          .mean().values
        
        mean_year_sub = lambda x: x - series_mean_year

        series_deseasonalized = series.groupby(series.index.year, 
                                               group_keys=False) \
                                               .apply(mean_year_sub)

        series = series_deseasonalized

    series_roll = series.rolling(window).agg(agg_method) if rolling else series

    ref_slice = slice(valid_start, None) if reftime is None else slice(reftime[0], reftime[1])

    series_roll_ref = series_roll.loc[ref_slice]
    
    series_roll_valid = series_roll.loc[valid_start:]

    dummy_out = np.array([np.nan] * len(series_roll_valid)) 

    if ((distribution == 'gamma') and 
        (np.any(series_roll_ref < 0) or 
         np.all(series_roll_ref == 0))): print('dummy out'); return dummy_out

    if np.all(np.isnan(series_roll_ref)): print('dummy out'); return dummy_out

    if np.all(series_roll_ref == series_roll_ref.iloc[0]): print('dummy out'); return dummy_out

    if distribution == 'gaussian_kde':

        pdf_xs, pdf_ys = gauss_kde_pdf(series_roll_ref)

        cdf_xs, cdf_ys = gauss_kde_cdf(series_roll_ref)

    else:

        parameter = distribution_fit(series_roll_ref.to_numpy(), 
                                     distribution=distribution)

        pdf_xs, pdf_ys = distribution_pdf(distribution=distribution,
                                          parameter=parameter)

        cdf_xs, cdf_ys = distribution_cdf(distribution=distribution,
                                          parameter=parameter)

    pdf_normal_xs, pdf_normal_ys = distribution_pdf()

    cdf_normal_xs, cdf_normal_ys = distribution_cdf()

    series_roll_cdf = np.interp(series_roll_valid, 
                                cdf_xs, 
                                cdf_ys)

    series_roll_sxi = np.interp(series_roll_cdf, 
                                cdf_normal_ys, 
                                cdf_normal_xs)

    str_deseasonalize = 'deseasonalized' if deseasonalize else ''
    xunit = '' if unit is None else f'[{unit}]'

    if plot_distributions: 

        os.makedirs(plot_out_dir, exist_ok=True)

        plot_dist(pdf_xs, 
                  pdf_ys, 
                  series_roll_ref, 
                  xlabel=' '.join([f'{window}', 
                                   f'{agg_method}', 
                                   f'{str_deseasonalize}', 
                                   f'{variable}', 
                                   f'{xunit}']), 
                  ylabel='Probability density')
        
    if plot_sxi_ts:
         
        os.makedirs(plot_out_dir, exist_ok=True)

        plot_sxi(time_index,
                 pd.Series(series_roll_valid.index),
                 array,
                 series_roll_sxi,
                 ylabel=f'{variable} {xunit}',
                 plot_out_dir=plot_out_dir)

    return series_roll_sxi