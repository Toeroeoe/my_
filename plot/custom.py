

def map_EU3_point_locations(lats, lons, rotnpole_lat: float, rotnpole_lon: float, semmj_axis: int, semmn_axis: int,
                        lon_extents: list, lat_extents: list, lw_grid: float = 0.5, lw_coast: float = 0.5,  color_grid: str = 'gray',
                        ls_grid: str = '--', xticks: list = [], yticks: list = [], fs_label: float = 10, size_marker: float = 4.0, 
                        marker: str = 'x', color_marker: str = 'firebrick', alpha: float = 0.7, zorder: int = 5, title: str = ''):

    from my_.figures.single import square
    from my_.plot.style import style_1
    from my_.plot.maps import EU3_plot_lines, map_point_locations
    from my_.plot.init_ax import EU3_plot_init

    print('Plot locations map...\n')

    style_1()
    
    rp, pc, xs, ys              = EU3_plot_init(rotnpole_lat, rotnpole_lon, semmj_axis, semmn_axis, lon_extents, lat_extents)

    figure, ax                  = square(projection = rp)

    ax.set_title(title)
    
    sizes                       = [size_marker] * len(lats)

    EU3_plot_lines(ax, pc, xs, ys, lw_grid, lw_coast, color_grid, ls_grid, xticks, yticks, fs_label)

    map_point_locations(ax, lats, lons, sizes, marker = marker, color = color_marker, projection = pc, alpha = alpha, zorder = zorder)

    return figure


def double_EU3_mesh_div_cbar(arrays, lat, lon,
                            rotnpole_lat: float, rotnpole_lon: float, semmj_axis: int, semmn_axis: int,
                            lon_extents: list, lat_extents: list,
                            lw_grid: float = 0.5, lw_coast: float = 0.5,  color_grid: str = 'gray',
                            ls_grid: str = '--', xticks: list = [], yticks: list = [], fs_label: float = 10,
                            cmap: str = 'coolwarm_r', cmap_n: int = 1000, v0: float = None, v1: float = None, 
                            extend: str = 'both', title: str = '', subtitles: list = [], clabel: str = '',
                            fs_title: float = 12, fs_subtitle: float = 10, fs_cbar_label: float = 10):
    

    from my_.plot.style import style_1
    from my_.figures.double import horizontal_cax
    from my_.plot.basic import colormesh
    from my_.plot.maps import EU3_plot_lines
    from my_.plot.init_ax import EU3_plot_init
    from my_.plot.colors import colormap, colorbar

    style_1()

    rp, pc, xs, ys              = EU3_plot_init(rotnpole_lat, rotnpole_lon, semmj_axis, semmn_axis, lon_extents, lat_extents)

    fig, axes, cax              = horizontal_cax(projection = rp)

    label_sides                 = [['bottom'], ['bottom', 'right']]

    cmap_c                      = colormap(cmap, cmap_n)

    fig.suptitle(title, fontsize = fs_title)

    for i_ax, ax in enumerate(axes):

        ax.set_title(subtitles[i_ax], fontsize = fs_subtitle)
        
        EU3_plot_lines(ax, pc, xs, ys, lw_grid, lw_coast, color_grid, ls_grid, xticks, yticks,
                       fs_label, label_sides = label_sides[i_ax])

        artist                  = colormesh(ax, lon, lat, arrays[i_ax], cmap_c, v0, v1, projection = pc)

    colorbar(cax, artist, clabel, pad = 10, extend = extend, fs_label = fs_cbar_label)

    return fig


def single_EU3_mesh_cat_cbar(array, lat, lon,
                            rotnpole_lat: float, rotnpole_lon: float, semmj_axis: int, semmn_axis: int,
                            lon_extents: list, lat_extents: list,
                            lw_grid: float = 0.5, lw_coast: float = 0.5,  color_grid: str = 'gray',
                            ls_grid: str = '--', xticks: list = [], yticks: list = [], fs_label: float = 10,
                            cmap: str = 'cet_glasbey_hv', extend: str = 'neither', title: str = '', clabel: str = '', 
                            fs_title: float = 12, fs_cbar_label: float = 10, cbar_tick_labels: list = []): 

    import numpy as np
    from my_.plot.style import style_1
    from my_.plot.maps import EU3_plot_init, EU3_plot_lines
    from my_.figures.single import square_cax
    from my_.plot.colors import colormap, colorbar
    from my_.plot.basic import colormesh

    import cartopy.feature as cfeature

    label_sides                 =  ['bottom', 'right']

    style_1()

    rp, pc, xs, ys              = EU3_plot_init(rotnpole_lat, rotnpole_lon, semmj_axis, semmn_axis, lon_extents, lat_extents)

    figure, ax, cax             = square_cax(projection = rp)

    ax.add_feature(cfeature.OCEAN, edgecolor='face', facecolor='white', zorder = 2)

    cmap_n                      = np.max(array) + 1 # "maybe better": length of unique values. But not sure

    cmap_c                      = colormap(cmap, cmap_n)

    ax.set_title(title, fontsize = fs_title)

    EU3_plot_lines(ax, pc, xs, ys, lw_grid, lw_coast, color_grid, ls_grid, xticks, yticks,
                       fs_label, label_sides = label_sides)

    artist                      = colormesh(ax, lon, lat, array, cmap_c, projection = pc)

    colorbar(cax, artist, clabel, pad = 10, extend = extend, 
            fs_label = fs_cbar_label, tick_labels = cbar_tick_labels)

    return figure


def xy_landcover_moments(df, variable, sources_insitu: list = [], sources_grids: list = [], 
                        sel_landcover: list = [], markers: dict = {}, colors: dict = {},
                        xy_init_args = {}, xy_args = {}, marker_legend_args = {}, color_legend_args = {},
                        moments = ['mean', 'var', 'skew', 'kurtosis']):

    from my_.figures.two_by_two import square_two_top_cax
    from my_.series.group import select_multi_index, nona_level
    from my_.plot.init_ax import init_xy
    from my_.plot.basic import scatter
    from my_.plot.legend import marker_legend, color_legend
    from my_.series.convert import tile_df_to_list

    from my_.resources.sources import query_variables

    import colorcet as cc

    print('Plot land cover aggregated xy plots...\n')

    df_nona                     = nona_level(df, ['Variable', 'Station'])

    df_i                        = select_multi_index(df_nona, ['Source', 'Variable', 'Landcover'],
                                                      keys = [sources_insitu, variable, sel_landcover])

    df_d                        = select_multi_index(df_nona, ['Source', 'Variable', 'Landcover'],
                                                      keys = [sources_grids, variable, sel_landcover])
    
    df_i_lc                     = df_i.groupby(axis = 1, level = ['Source', 'Landcover']).mean()
    df_d_lc                     = df_d.groupby(axis = 1, level = ['Source', 'Landcover']).mean()

    i_sources                   = df_i_lc.columns.unique(level = 'Source')
    d_sources                   = df_d_lc.columns.unique(level = 'Source')

    cmapc                       = cc.glasbey_hv[:]

    var_units                   = query_variables(i_sources[0], 'var_units')[variable]

    mom_units                   = [var_units, var_units, '-', '-']

    if len(i_sources) > 1: raise NotImplementedError

    fig, axs, axs_l             = square_two_top_cax()

    colors                      = {k: v for k,v in colors.items() if k in d_sources}

    marker_legend(axs_l[0], markers, **marker_legend_args)
    color_legend(axs_l[1], colors, cmapc, **color_legend_args)

    for iax, ax in enumerate(axs):

        agg_moment              = moments[iax]
        
        df_i_lc_agg             = df_i_lc.agg(agg_moment)
        df_d_lc_agg             = df_d_lc.agg(agg_moment)

        title_fig               = ''

        xlabel                  = f'Observation [{mom_units[iax]}]'
        ylabel                  = f'Model [{mom_units[iax]}]'

        init_xy(ax, df_i_lc_agg, df_d_lc_agg, title = title_fig, 
                xlabel = xlabel, ylabel = ylabel, ax_tag = agg_moment,
                **xy_init_args)

        for lc in df_i.columns.unique(level = 'Landcover'):

            colorsc                 = [cmapc[colors[d]] for d in d_sources]

            ys                      = select_multi_index(df_d_lc_agg, 'Landcover', lc, axis = 0)

            xs                      = select_multi_index(df_i_lc_agg, 'Landcover', lc, axis = 0)
            
            xs_tile                 = tile_df_to_list(xs, len(d_sources))

            scatter(ax, xs_tile, ys, markers[lc], colors_marker = colorsc, **xy_args)  
    
    return fig


def bar_rmse_landcover(df, variable, sources_insitu, sources_grids, sel_landcover,
                       colors: dict = {}, bar_init_args = {}, bar_args = {},
                       color_legend_args = {}):

    from my_.series.group import select_multi_index, nona_level
    from my_.series.aggregate import column_wise
    from my_.math.stats import rmse, mean
    from my_.resources.sources import query_variables

    from my_.figures.two_by_two import square_top_cax
    from my_.plot.basic import bar
    from my_.plot.init_ax import init_bar
    from my_.plot.legend import color_legend

    import numpy as np
    import colorcet as cc

    print('Plot land cover aggregated rmse bar plots...\n')

    df_nona                     = nona_level(df, ['Variable', 'Station'])

    df_s                        = select_multi_index(df_nona, ['Variable', 'Landcover'],
                                                      keys = [variable, sel_landcover])
    
    df_s                        = df_s.reindex(labels = sources_insitu + sources_grids, axis = 1, level = 'Source')
    
    df_lc_rmse                  = df_s.groupby(axis = 1, level = ['Source', 'Landcover']).apply(column_wise, ffunc = rmse)

    df_lc_rmse_mean             = df_lc_rmse.groupby(axis = 1, level = ['Source', 'Landcover']).apply(mean, axes = (0, 1))

    sources                     = df_lc_rmse_mean.index.unique(level = 'Source')

    var_units                   = query_variables(sources[0], 'var_units')[variable]
    
    fig, axs, axs_l             = square_top_cax()

    cmapc                       = cc.glasbey_hv[:]

    colors                      = {k: v for k,v in colors.items() if k in sources}
    colorsc                     = [cmapc[colors[d]] for d in list(sources)]

    color_legend(axs_l, colors, cmapc, **color_legend_args)

    xs                          = np.arange(len(sources))

    ys                          = df_lc_rmse_mean
    
    for iax, ax in enumerate(axs):

        lc                      = sel_landcover[iax]

        ys_lc                   = select_multi_index(ys, levels = ['Landcover'], keys = [lc], axis = 0)

        init_bar(ax, xs, ys, ax_tag = lc, ylabel = f'RMSD [{var_units}]', **bar_init_args)

        bar(ax, xs, ys_lc, color = colorsc, **bar_args)
    
    return fig


def doy_dist_landcover(name, df, variable, sources_insitu, sources_grids, sel_landcover,
                       colors: dict = {}, doy_init_args = {}, dist_init_args = {},
                       doy_args = {}, dist_args = {}, doy_fill_args = {},
                       color_legend_args = {}, do_fill = True, do_line_bounds = False):


    from my_.series.group import select_multi_index, nona_level
    from my_.series.aggregate import column_wise

    from my_.math.stats import gauss_kde_pdf, pbias, rmse
    from my_.resources.sources import query_variables

    from my_.figures.four_by_two import vertical_top_cax
    from my_.plot.init_ax import init_ts, init_dist
    from my_.plot.legend import color_legend
    from my_.plot.basic import plot, fill 
    from my_.files.handy import save_df 

    import colorcet as cc

    print('Plot land cover aggregated DOY and distribution plots...\n')
    
    df_nona                     = nona_level(df, ['Variable', 'Station'])

    df_s                        = select_multi_index(df_nona, ['Variable', 'Landcover'],
                                                      keys = [variable, sel_landcover])
    
    df_s                        = df_s.reindex(labels = sources_insitu + sources_grids, axis = 1, level = 'Source')

    sources                     = df_s.columns.unique(level = 'Source')

    df_doy                      = df_s.groupby(df_s.index.dayofyear).mean()

    df_doy_lc                   = df_doy.groupby(axis = 1, level = ['Source', 'Landcover'])

    df_doy_lc_mean              = df_doy_lc.mean()

    df_doy_lc_mean_rmse        = column_wise(df_doy_lc_mean, ffunc = rmse)
    df_doy_lc_mean_pbias        = column_wise(df_doy_lc_mean, ffunc = pbias)
    save_df(df_doy_lc_mean_rmse, f'out/{name}/csv/doy_lc_mean_rmse_{variable}.csv', format = 'csv')
    save_df(df_doy_lc_mean_pbias, f'out/{name}/csv/doy_lc_mean_pbias_{variable}.csv', format = 'csv')

    df_doy_lc_std               = df_doy_lc.std()

    df_dist_lc                  = df_s.groupby(axis = 1, level = ['Source', 'Landcover']).apply(gauss_kde_pdf)

    df_dist_lc.columns          = df_dist_lc.columns.set_names('pdf', level = -1)

    all_xs                      = select_multi_index(df_dist_lc, 'pdf', 'xs')
    all_ys                      = select_multi_index(df_dist_lc, 'pdf', 'ys')

    fig, axs, axs_l             = vertical_top_cax(fy = 8)

    var_units                   = query_variables(sources[0], 'var_units')[variable]

    cmapc                       = cc.glasbey_hv[:]
    colors                      = {k: v for k,v in colors.items() if k in sources}
    colorsc                     = [cmapc[colors[d]] for d in list(sources)]

    color_legend(axs_l, colors, cmapc, **color_legend_args)

    for ilc, lc in enumerate(sel_landcover):

        xs_doy                  = df_doy_lc_mean.index

        ys_doy                  = select_multi_index(df_doy_lc_mean, levels = ['Landcover'], keys = [lc])
        
        err_doy                 = select_multi_index(df_doy_lc_std, levels = ['Landcover'], keys = [lc])

        xs_dist                 = select_multi_index(df_dist_lc, levels = ['Landcover', 'pdf'], keys = [lc, 'xs'])

        ys_dist                 = select_multi_index(df_dist_lc, levels = ['Landcover', 'pdf'], keys = [lc, 'ys'])

        var_label               = f'{variable} [{var_units}]'

        lower                   = ys_doy - err_doy
        upper                   = ys_doy + err_doy

        init_ts(axs[ilc, 0], xs_doy, df_doy_lc_mean, ylabel = var_label, ax_tag = lc, **doy_init_args)
        init_dist(axs[ilc, 1], all_xs, all_ys, xlabel = var_label, ax_tag = lc, **dist_init_args)

        plot(axs[ilc, 0], xs_doy, ys_doy, colors = colorsc, **doy_args)
        if do_fill : fill(axs[ilc, 0], xs_doy, lower, upper, colors = colorsc, **doy_fill_args)

        if do_line_bounds:
            plot(axs[ilc, 0], xs_doy, lower, colors = colorsc, style = '-.', alpha = 0.6, lw = 1.0, zorder = 6)
            plot(axs[ilc, 0], xs_doy, upper, colors = colorsc, style = '-.', alpha = 0.6, lw = 1.0, zorder = 6)
        plot(axs[ilc, 1], xs_dist, ys_dist, colors = colorsc, **dist_args)
        
    return fig


def pie_landcover(df_static, selected_landcover, colors = {}, color_legend_args = {}):

    print('Plot network land cover pie plots\n')

    from my_.series.aggregate import concat
    from my_.resources.sources import query_static

    from my_.figures.double import horizontal_top_cax
    from my_.plot.basic import pie
    from my_.plot.legend import color_legend

    from my_.plot.init_ax import init_pie

    import matplotlib.pyplot as plt

    landcover                   = df_static['landcover'].where(df_static['landcover'].isin(selected_landcover))

    pct_crop                    = df_static['PCT_CROP'] / 100

    pct_nat                     = df_static['PCT_NATVEG'] / 100

    pft_cols                    = [col for col in df_static.columns if 'PCT_NAT_PFT_' in col]

    cft_cols                    = [col for col in df_static.columns if 'PCT_CFT_' in col]

    pft_rel                     = df_static[pft_cols].multiply(pct_nat, axis = 0)

    cft_rel                     = df_static[cft_cols].multiply(pct_crop, axis = 0)

    df_tot                      = concat([pft_rel, cft_rel], sort = False)

    ind_landcover               = query_static('CLM5-EU3-surf', 'sel_agg_layer_PFT')

    shares_surf                 = [df_tot.iloc[:, ind_landcover[lc]].sum(axis = 1).mean() for lc in selected_landcover]

    shares_surf_o               = shares_surf + [100 - sum(shares_surf)] 

    shares_lc                   = landcover.value_counts(normalize = True)

    fig, axs, axl               = horizontal_top_cax(x_an = 0.1, y_an = 0.8)

    cmapc                       = plt.cm.get_cmap('Set2').colors

    colors                      = {k: v for k,v in colors.items()}
    colorsc                     = [cmapc[colors[lc]] for lc in list(selected_landcover)]

    colors['other']             = 7

    colorsc_o                   = colorsc + [cmapc[7]]

    color_legend(axl, colors, cmapc, **color_legend_args)

    init_pie(axs[0], ax_tag = 'ICOS network')
    init_pie(axs[1], ax_tag = 'Corresponding CLM5 surface')

    pie(axs[0], shares_lc, colorsc)
    pie(axs[1], shares_surf_o, colorsc_o)

    return fig


def doy_landcover(df, variable, sources_insitu, sources_grids, sel_landcover,
                       colors: dict = {}, doy_init_args = {},
                       doy_args = {}, doy_fill_args = {},
                       color_legend_args = {}, do_fill = False):
    
    print('Plot network land cover DOY plots\n')

    from my_.series.group import select_multi_index, nona_level
    from my_.resources.sources import query_variables

    from my_.figures.two_by_two import square_top_cax
    from my_.plot.init_ax import init_ts
    from my_.plot.legend import color_legend
    from my_.plot.basic import plot, fill 

    import colorcet as cc

    df_nona                     = nona_level(df, ['Variable', 'Station'])

    df_s                        = select_multi_index(df_nona, ['Variable', 'Landcover'],
                                                      keys = [variable, sel_landcover])
    
    df_s                        = df_s.reindex(labels = sources_insitu + sources_grids, axis = 1, level = 'Source')

    sources                     = df_s.columns.unique(level = 'Source')

    df_doy                      = df_s.groupby(df_s.index.dayofyear).mean()

    df_doy_lc                   = df_doy.groupby(axis = 1, level = ['Source', 'Landcover'])

    df_doy_lc_mean              = df_doy_lc.mean()

    df_doy_lc_std               = df_doy_lc.std()

    fig, axs, axl               = square_top_cax()

    var_units                   = query_variables(sources[0], 'var_units')[variable]

    cmapc                       = cc.glasbey_hv[:]
    colors                      = {k: v for k,v in colors.items() if k in sources}
    colorsc                     = [cmapc[colors[d]] for d in list(sources)]

    color_legend(axl, colors, cmapc, **color_legend_args)

    for ilc, lc in enumerate(sel_landcover):

        xs_doy                  = df_doy_lc_mean.index

        ys_doy                  = select_multi_index(df_doy_lc_std, levels = ['Landcover'], keys = [lc])
        
        err_doy                 = select_multi_index(df_doy_lc_std, levels = ['Landcover'], keys = [lc])

        var_label               = f'{variable} [{var_units}]'

        lower                   = ys_doy - err_doy
        upper                   = ys_doy + err_doy

        init_ts(axs[ilc], xs_doy, df_doy_lc_std, ylabel = var_label, ax_tag = lc, **doy_init_args)
        plot(axs[ilc], xs_doy, ys_doy, colors = colorsc, **doy_args)

        if do_fill: fill(axs[ilc], xs_doy, lower, upper, colors = colorsc, **doy_fill_args)

    return fig


def plot_ts(df, variable, station, colors: dict = {}, color_legend_args: dict = {},
            fig_args: dict = {}, ts_init_args: dict = {}, plot_args: dict = {}):

    print(f'Plot station time-series: {station}, {variable}\n')

    from my_.series.group import select_multi_index, nona_level
    from my_.figures.single import square_top_cax
    from my_.plot.init_ax import init_ts_2
    from my_.plot.basic import plot
    from my_.plot.legend import color_legend
    from my_.resources.sources import query_variables

    import colorcet as cc
    import numpy as np

    df_nona                     = nona_level(df, ['Variable', 'Station'])

    df_s                        = select_multi_index(df_nona, ['Variable', 'Station'],
                                                      keys = [variable, station])
    
    sources                     = df_s.columns.unique(level = 'Source')
    
    cmapc                       = cc.glasbey_hv[:]
    colors                      = {k: v for k,v in colors.items() if k in sources}
    colorsc                     = [cmapc[colors[d]] for d in list(sources)]

    fig, ax, axl                = square_top_cax(**fig_args)

    var_units                   = query_variables(sources[0], 'var_units')[variable]

    xs                          = df_s.index
    ys                          = df_s

    if np.all(np.isnan(ys)): return fig
    
    color_legend(axl, colors, cmapc, **color_legend_args)

    init_ts_2(ax, df_s.dropna(how = 'all').index, df_s.dropna(how = 'all'),
            title = f'{station} {variable} [{var_units}]', **ts_init_args)

    plot(ax, xs, ys, colors = colorsc, **plot_args)

    return  fig