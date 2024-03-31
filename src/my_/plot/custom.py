import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

def map_EU3_point_locations_lc_hclim(lats, lons, landcover, hydroclimate, rotnpole_lat: float, rotnpole_lon: float, semmj_axis: int, semmn_axis: int,
                        lon_extents: list, lat_extents: list, lw_grid: float = 0.5, lw_coast: float = 0.5,  color_grid: str = 'gray',
                        ls_grid: str = '--', xticks: list = [], yticks: list = [], fs_label: float = 10, size_marker: float = 4.0, 
                        marker: str = 'x', color_marker: str = 'firebrick', alpha: float = 0.85, zorder: int = 5, title: str = '',
                        marker_legend_args: dict = {}):

    from my_figures.single import square_top_right_cax
    from my_plot.style import style_1
    from my_plot.maps import EU3_plot_lines, map_point_locations
    from my_plot.init_ax import EU3_plot_init
    from my_plot.colors import colorbar
    from my_plot.legend import marker_legend
    from user_in.options_analyses import selected_landcover, markers
    
    import matplotlib.pyplot as plt
    import matplotlib as mpl

    print('Plot locations map...\n')

    style_1()
    
    rp, pc, xs, ys              = EU3_plot_init(rotnpole_lat, rotnpole_lon, semmj_axis, semmn_axis, lon_extents, lat_extents)

    figure, ax, caxt, caxr      = square_top_right_cax(projection = rp, fy = 5.0)

    ax.set_title(title)
    
    sizes                       = [size_marker] * len(lats)

    cmap                        = plt.get_cmap('BrBG', 6)

    EU3_plot_lines(ax, pc, xs, ys, lw_grid, lw_coast, color_grid, ls_grid, xticks, yticks, fs_label)

    for lc in landcover.unique():
        
        if lc not in selected_landcover: continue

        lat_lc                  = lats.where(landcover == lc)
        lon_lc                  = lons.where(landcover == lc)
        hclim_lc                = hydroclimate.where(landcover == lc)

        colors                  = [cmap(hc/6) for hc in hclim_lc]

        map_point_locations(ax, lat_lc, lon_lc, sizes, marker = markers[lc], color = colors, projection = pc, alpha = alpha, zorder = zorder)

        a = mpl.cm.ScalarMappable(norm = mpl.colors.Normalize(vmin=0, vmax=5), cmap = cmap) 
        ticks = ['Very arid', 'Arid', 'Semi arid', 'Semi humid', 'Humid', 'Very humid']

    colorbar(caxr, a, '', pad = 10, extend = 'neither', fs_label = 12, tick_labels = ticks)
    marker_legend(caxt, markers, **marker_legend_args)

    return figure


def map_EU3_point_locations_hclim(lats, lons, hydroclimate, rotnpole_lat: float, rotnpole_lon: float, semmj_axis: int, semmn_axis: int,
                        lon_extents: list, lat_extents: list, lw_grid: float = 0.5, lw_coast: float = 0.5,  color_grid: str = 'gray',
                        ls_grid: str = '--', xticks: list = [], yticks: list = [], fs_label: float = 10, size_marker: float = 45, 
                        marker: str = 'o', alpha: float = 0.85, zorder: int = 5, title: str = ''):

    from my_figures.single import square_right_cax
    from my_plot.style import style_1
    from my_plot.maps import EU3_plot_lines, map_point_locations
    from my_plot.init_ax import EU3_plot_init
    from my_plot.colors import colorbar
    
    import matplotlib.pyplot as plt
    import matplotlib as mpl

    print('Plot locations map...\n')

    style_1()
    
    rp, pc, xs, ys              = EU3_plot_init(rotnpole_lat, rotnpole_lon, semmj_axis, semmn_axis, lon_extents, lat_extents)

    figure, ax, cax             = square_right_cax(projection = rp, fy = 5.0)

    ax.set_title(title)
    
    sizes                       = [size_marker] * len(lats)

    cmap                        = plt.get_cmap('BrBG', 6)

    EU3_plot_lines(ax, pc, xs, ys, lw_grid, lw_coast, color_grid, ls_grid, xticks, yticks, fs_label)
    
    colors                  = [cmap(hc/6) for hc in hydroclimate]

    map_point_locations(ax, lats, lons, sizes, marker = marker, color = colors, projection = pc, alpha = alpha, zorder = zorder)

    a = mpl.cm.ScalarMappable(norm = mpl.colors.Normalize(vmin=0, vmax=5), cmap = cmap) 
    ticks = ['Very arid', 'Arid', 'Semi arid', 'Semi humid', 'Humid', 'Very humid']

    colorbar(cax, a, '', pad = 10, extend = 'neither', fs_label = 12, tick_labels = ticks)

    return figure


def map_EU3_point_locations(lats, lons, rotnpole_lat: float, rotnpole_lon: float, semmj_axis: int, semmn_axis: int,
                        lon_extents: list, lat_extents: list, lw_grid: float = 0.5, lw_coast: float = 0.5,  color_grid: str = 'gray',
                        ls_grid: str = '--', xticks: list = [], yticks: list = [], fs_label: float = 10, size_marker: float = 4.0, 
                        marker: str = 'x', color_marker: str = 'firebrick', alpha: float = 0.7, zorder: int = 5, title: str = ''):

    from my_figures.single import square
    from my_plot.style import style_1
    from my_plot.maps import EU3_plot_lines, map_point_locations
    from my_plot.init_ax import EU3_plot_init

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
    

    from my_plot.style import style_1
    from my_figures.double import horizontal_cax
    from my_plot.basic import colormesh
    from my_plot.maps import EU3_plot_lines
    from my_plot.init_ax import EU3_plot_init
    from my_plot.colors import colormap, colorbar

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

def single_EU3_mesh_div_cbar(array, lat, lon,
                            rotnpole_lat: float, rotnpole_lon: float, semmj_axis: int, semmn_axis: int,
                            lon_extents: list, lat_extents: list,
                            lw_grid: float = 0.5, lw_coast: float = 0.5,  color_grid: str = 'gray',
                            ls_grid: str = '--', xticks: list = [], yticks: list = [], fs_label: float = 10,
                            cmap: str = 'coolwarm_r', cmap_n: int = 1000, v0: float = None, v1: float = None, 
                            extend: str = 'both', title: str = '', subtitle: str = '', clabel: str = '',
                            fs_title: float = 12, fs_subtitle: float = 10, fs_cbar_label: float = 10):
    

    from my_.plot.style import style_1
    from my_.figures.single import square_right_cax
    from my_.plot.basic import colormesh
    from my_.plot.maps import EU3_plot_lines
    from my_.plot.init_ax import EU3_plot_init
    from my_.plot.colors import colormap, colorbar

    rp, pc, xs, ys              = EU3_plot_init(rotnpole_lat, rotnpole_lon, semmj_axis, semmn_axis, lon_extents, lat_extents)

    fig, ax, cax                = square_right_cax(projection = rp)

    label_sides                 = ['bottom', 'right']

    cmap_c                      = colormap(cmap, cmap_n)

    fig.suptitle(title, fontsize = fs_title)


    ax.set_title(subtitle, fontsize = fs_subtitle)
        
    EU3_plot_lines(ax, pc, xs, ys, lw_grid, lw_coast, color_grid, ls_grid, xticks, yticks,
                    fs_label, label_sides = label_sides)

    artist                  = colormesh(ax, lon, lat, array, cmap_c, v0, v1, projection = pc)

    colorbar(cax, artist, clabel, pad = 10, extend = extend, fs_label = fs_cbar_label)

    return fig

def pie_location_lc_clim_map(df_static: pd.DataFrame,
                            lats: np.ndarray | list | tuple | pd.Series,
                            lons: np.ndarray | list | tuple | pd.Series,
                            landcover: np.ndarray | list | tuple | pd.Series,
                            hydroclimate: np.ndarray | list | tuple | pd.Series,
                            basemap_args: dict, 
                            baselines_args: dict, 
                            map_args: dict,
                            markers: dict,
                            marker_legend_args: dict,
                            selected_landcover: list[str], 
                            colors: dict,
                            color_legend_args:dict) -> plt.figure:
    
    from my_figures.one_by_three import horizontal_right_map_two_cax
    from my_series.aggregate import concat
    from my_plot.basic import pie
    from my_plot.init_ax import init_pie, EU3_plot_init
    from my_plot.legend import color_legend, marker_legend
    from my_plot.colors import colorbar
    from my_resources.sources import query_static
    from my_plot.maps import EU3_plot_lines, map_point_locations

    rp, pc, xs, ys              = EU3_plot_init(**basemap_args)

    fig, axs, axl1, axl2, axc   = horizontal_right_map_two_cax(projection = rp)

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

    cmapc                       = plt.cm.get_cmap('Set2').colors

    colors                      = {k: v for k,v in colors.items()}
    colorsc                     = [cmapc[colors[lc]] for lc in list(selected_landcover)]

    colors['other']             = 7

    colorsc_o                   = colorsc + [cmapc[7]]

    color_legend(axl1, colors, cmapc, **color_legend_args)

    init_pie(axs[0], ax_tag = 'ICOS network')
    init_pie(axs[1], ax_tag = 'CLM5 surface')

    pie(axs[0], shares_lc, colorsc, autopct='%1.1f%%')
    pie(axs[1], shares_surf_o, colorsc_o, autopct='%1.1f%%')

    sizes                       = [map_args['size_marker']] * len(lats)

    cmap                        = plt.get_cmap('BrBG', 6)

    EU3_plot_lines(axs[-1], pc, xs, ys, **baselines_args)
    
    for lc in landcover.unique():
        
        if lc not in selected_landcover: continue

        lat_lc                  = lats.where(landcover == lc)
        lon_lc                  = lons.where(landcover == lc)
        hclim_lc                = hydroclimate.where(landcover == lc)

        colors                  = [cmap(hc/6) for hc in hclim_lc]

        map_point_locations(axs[2], lat_lc, lon_lc, sizes, marker = markers[lc], color = colors, projection = pc, alpha = map_args['alpha'], zorder = map_args['zorder'])

        a = mpl.cm.ScalarMappable(norm = mpl.colors.Normalize(vmin=0, vmax=5), cmap = cmap) 
        ticks = ['Very\narid', 'Arid', 'Semi\narid', 'Semi\nhumid', 'Humid', 'Very\nhumid']

    colorbar(axc, a, '', pad = 10, extend = 'neither', fs_label = 8, tick_labels = ticks, orientation = 'horizontal')
    marker_legend(axl2, markers, **marker_legend_args)

    return fig



def single_EU3_mesh_cat_cbar(array, lat, lon,
                            rotnpole_lat: float, rotnpole_lon: float, semmj_axis: int, semmn_axis: int,
                            lon_extents: list, lat_extents: list,
                            lw_grid: float = 0.5, lw_coast: float = 0.5,  color_grid: str = 'gray',
                            ls_grid: str = '--', xticks: list = [], yticks: list = [], fs_label: float = 10,
                            cmap: str = 'cet_glasbey_hv', extend: str = 'neither', title: str = '', clabel: str = '', 
                            fs_title: float = 12, fs_cbar_label: float = 10, cbar_tick_labels: list = []): 

    import numpy as np
    from my_plot.style import style_1
    from my_plot.maps import EU3_plot_lines
    from my_plot.init_ax import EU3_plot_init
    from my_figures.single import square_right_cax
    from my_plot.colors import colormap, colorbar
    from my_plot.basic import colormesh

    import cartopy.feature as cfeature

    label_sides                 =  ['bottom', 'right']

    style_1()

    rp, pc, xs, ys              = EU3_plot_init(rotnpole_lat, rotnpole_lon, semmj_axis, semmn_axis, lon_extents, lat_extents)

    figure, ax, cax             = square_right_cax(projection = rp)

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


def single_EU3_mesh_cont_cbar(array, lat, lon,
                            rotnpole_lat: float, rotnpole_lon: float, semmj_axis: int, semmn_axis: int,
                            lon_extents: list, lat_extents: list,
                            lw_grid: float = 0.5, lw_coast: float = 0.5,  color_grid: str = 'gray',
                            ls_grid: str = '--', xticks: list = [], yticks: list = [], fs_label: float = 10,
                            cmap: str = 'Greens', extend: str = 'neither', title: str = '', clabel: str = '', 
                            fs_title: float = 12, fs_cbar_label: float = 10, cbar_tick_labels: list = []): 

    import numpy as np
    from my_plot.style import style_1
    from my_plot.maps import EU3_plot_lines
    from my_plot.init_ax import EU3_plot_init
    from my_figures.single import square_right_cax
    from my_plot.colors import colormap, colorbar
    from my_plot.basic import colormesh

    import cartopy.feature as cfeature

    label_sides                 =  ['bottom', 'right']

    style_1()

    rp, pc, xs, ys              = EU3_plot_init(rotnpole_lat, rotnpole_lon, semmj_axis, semmn_axis, lon_extents, lat_extents)

    figure, ax, cax             = square_right_cax(projection = rp)

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
                        moments = ['mean', 'variance', 'skewness', 'kurtosis']):

    from my_figures.two_by_two import square_two_top_cax
    from my_series.group import select_multi_index, nona_level
    from my_plot.init_ax import init_xy
    from my_plot.basic import scatter, error
    from my_plot.legend import marker_legend, color_legend
    from my_series.convert import tile_df_to_list

    from my_resources.sources import query_variables

    from my_math import stats

    import colorcet as cc
    import numpy as np

    print('Plot land cover aggregated xy plots...\n')

    df_nona                     = nona_level(df, ['Variable', 'Station'])

    df_i                        = select_multi_index(df_nona, ['Source', 'Variable', 'Landcover'],
                                                      keys = [sources_insitu, variable, sel_landcover])

    df_d                        = select_multi_index(df_nona, ['Source', 'Variable', 'Landcover'],
                                                      keys = [sources_grids, variable, sel_landcover])
    
    df_i_lc                     = df_i.groupby(axis = 1, level = ['Source', 'Landcover'])#.mean()
    df_d_lc                     = df_d.groupby(axis = 1, level = ['Source', 'Landcover'])#.mean()

    i_sources                   = df_i_lc.obj.columns.unique(level = 'Source')
    d_sources                   = df_d_lc.obj.columns.unique(level = 'Source')

    cmapc                       = cc.glasbey_hv[:]

    var_units                   = query_variables(i_sources[0], 'var_units')[variable]

    mom_units                   = [f'[{var_units}]', f'[{var_units}]²', '[-]', '[-]']

    if len(i_sources) > 1: raise NotImplementedError

    fig, axs, axs_l             = square_two_top_cax()

    labels_sources              = {s: query_variables(s, 'name_label') for s in d_sources}

    colors                      = {labels_sources[k]: v for k,v in colors.items() if k in d_sources}

    marker_legend(axs_l[0], markers, **marker_legend_args)
    color_legend(axs_l[1], colors, cmapc, nrows = np.ceil(len(d_sources) / 3), **color_legend_args)

    for iax, ax in enumerate(axs):

        agg_moment              = moments[iax]

        agg_method              = getattr(stats, agg_moment)
        err_method              = getattr(stats, f'std_error_{agg_moment}')
        
        #df_i_lc_agg             = df_i_lc.agg(agg_moment)
        #df_d_lc_agg             = df_d_lc.agg(agg_moment)

        df_i_lc_agg             = df_i_lc.apply(agg_method)
        df_d_lc_agg             = df_d_lc.apply(agg_method)

        df_i_lc_agg_err         = df_i_lc.apply(err_method)
        df_d_lc_agg_err         = df_d_lc.apply(err_method)

        title_fig               = ''

        xlabel                  = f'Observation {mom_units[iax]}'
        ylabel                  = f'Model {mom_units[iax]}'

        init_xy(ax, df_i_lc_agg, df_d_lc_agg, title = title_fig, 
                xlabel = xlabel, ylabel = ylabel, ax_tag = agg_moment,
                **xy_init_args)

        for lc in df_i.columns.unique(level = 'Landcover'):

            colorsc                 = [cmapc[colors[d]] for d in colors.keys()]

            ys                      = select_multi_index(df_d_lc_agg, 'Landcover', lc, axis = 0)

            xs                      = select_multi_index(df_i_lc_agg, 'Landcover', lc, axis = 0)

            x_err                   = select_multi_index(df_i_lc_agg_err, 'Landcover', lc, axis = 0)

            y_err                   = select_multi_index(df_d_lc_agg_err, 'Landcover', lc, axis = 0)
            
            xs_tile                 = tile_df_to_list(xs, len(d_sources))

            scatter(ax, xs_tile, ys, markers[lc], colors_marker = colorsc, **xy_args)
            error(ax, xs_tile, ys, x_err = x_err, y_err = y_err, ecolors = colorsc, elinewidth = 2)
    
    return fig


def bar_rmse_landcover(df, variable, sources_insitu, sources_grids, sel_landcover,
                       colors: dict = {}, bar_init_args = {}, bar_args = {},
                       color_legend_args = {}):

    from my_series.group import select_multi_index, nona_level
    from my_series.aggregate import column_wise
    from my_math.stats import rmse, mean, std_deviation
    from my_resources.sources import query_variables

    from my_figures.two_by_two import square_top_cax
    from my_plot.basic import bar, error
    from my_plot.init_ax import init_bar
    from my_plot.legend import color_legend

    import numpy as np
    import colorcet as cc

    print('Plot land cover aggregated rmse bar plots...\n')

    df_nona                     = nona_level(df, ['Variable', 'Station'])

    df_s                        = select_multi_index(df_nona, ['Variable', 'Landcover'],
                                                      keys = [variable, sel_landcover])
    
    df_s                        = df_s.reindex(labels = sources_insitu + sources_grids, axis = 1, level = 'Source')
    
    df_lc_rmse                  = df_s.groupby(axis = 1, level = ['Source', 'Landcover']).apply(column_wise, ffunc = rmse)

    df_lc_rmse_mean             = df_lc_rmse.groupby(axis = 1, level = ['Source', 'Landcover']).apply(mean, axis = (0, 1))
    df_lc_rmse_std             = df_lc_rmse.groupby(axis = 1, level = ['Source', 'Landcover']).apply(std_deviation, axis = (0, 1))

    sources                     = df_lc_rmse_mean.index.unique(level = 'Source')

    var_units                   = query_variables(sources[0], 'var_units')[variable]
    labels_sources              = {s: query_variables(s, 'name_label') for s in sources}
    
    fig, axs, axs_l             = square_top_cax()

    cmapc                       = cc.glasbey_hv[:]

    colors                      = {labels_sources[k]: v for k,v in colors.items() if k in sources}
    colorsc                     = [cmapc[colors[d]] for d in colors.keys()]

    color_legend(axs_l, colors, cmapc, **color_legend_args)

    xs                          = np.arange(len(sources))

    ys                          = df_lc_rmse_mean

    y_err                       = df_lc_rmse_std
    
    for iax, ax in enumerate(axs):

        lc                      = sel_landcover[iax]

        ys_lc                   = select_multi_index(ys, levels = ['Landcover'], keys = [lc], axis = 0)

        y_err_lc                = select_multi_index(y_err, levels = ['Landcover'], keys = [lc], axis = 0)

        ecolors                 = ['gray'] * len(ys_lc)

        init_bar(ax, xs, ys + y_err, ax_tag = lc, ylabel = f'RMSD [{var_units}]', **bar_init_args)

        bar(ax, xs, ys_lc, color = colorsc, **bar_args)
        
        error(ax, xs, ys_lc, y_err = y_err_lc, ecolors = ecolors, 
              capsize = 4, alpha = 0.8, zorder = 6)
    
    return fig


def doy_doy_landcover(name: str, 
                      df: pd.DataFrame,
                      variable: str,
                      sources_insitu: list[str], 
                      sources_grids: list[str], 
                      sel_landcover: list[str],
                      colors: dict = {}, 
                      doy_init_args: dict = {}, 
                      doy_args: dict = {}, 
                      doy_fill_args: dict = {},
                      color_legend_args: dict = {}, 
                      do_fill: bool = True, 
                      do_line_bounds: bool = False):

    from my_series.group import select_multi_index, nona_level
    from my_series.aggregate import column_wise

    from my_math.stats import gauss_kde_pdf, pbias, rmse
    from my_resources.sources import query_variables

    from my_figures.four_by_two import vertical_top_cax
    from my_plot.init_ax import init_ts, init_dist
    from my_plot.legend import color_legend
    from my_plot.basic import plot, fill 
    from my_files.handy import save_df 

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

    df_doy_lc_mean_rmse         = column_wise(df_doy_lc_mean, ffunc = rmse)
    df_doy_lc_mean_pbias        = column_wise(df_doy_lc_mean, ffunc = pbias)
    save_df(df_doy_lc_mean_rmse, f'out/{name}/csv/doy_lc_mean_rmse_{variable}.csv', format = 'csv')
    save_df(df_doy_lc_mean_pbias, f'out/{name}/csv/doy_lc_mean_pbias_{variable}.csv', format = 'csv')

    df_doy_lc_std               = df_doy_lc.std()

    fig, axs, axs_l             = vertical_top_cax(fy = 8)

    var_units                   = query_variables(sources[0], 'var_units')[variable]
    labels_sources              = {s: query_variables(s, 'name_label') for s in sources}

    cmapc                       = cc.glasbey_hv[:]
    colors                      = {labels_sources[k]: v for k,v in colors.items() if k in sources}
    colorsc                     = [cmapc[colors[d]] for d in colors.keys()]

    color_legend(axs_l, colors, cmapc, **color_legend_args)

    for ilc, lc in enumerate(sel_landcover):

        xs_doy                  = df_doy_lc_mean.index

        ys_doy                  = select_multi_index(df_doy_lc_mean, levels = ['Landcover'], keys = [lc])
        
        err_doy                 = select_multi_index(df_doy_lc_std, levels = ['Landcover'], keys = [lc])

        var_label               = f'{variable} [{var_units}]'

        init_ts(axs[ilc, 0], xs_doy, df_doy_lc_mean, ylabel = f'mean {var_label}', ax_tag = lc, **doy_init_args)
        init_ts(axs[ilc, 1], xs_doy, df_doy_lc_std, ylabel = f'std {var_label}', ax_tag = lc, **doy_init_args)

        plot(axs[ilc, 0], xs_doy, ys_doy, colors = colorsc, **doy_args)
        plot(axs[ilc, 1], xs_doy, err_doy, colors = colorsc, **doy_args)
        
    return fig

def doy_dist_landcover(name, df, variable, sources_insitu, sources_grids, sel_landcover,
                       colors: dict = {}, doy_init_args = {}, dist_init_args = {},
                       doy_args = {}, dist_args = {}, doy_fill_args = {},
                       color_legend_args = {}, do_fill = True, do_line_bounds = False):


    from my_series.group import select_multi_index, nona_level
    from my_series.aggregate import column_wise

    from my_math.stats import gauss_kde_pdf, pbias, rmse
    from my_resources.sources import query_variables

    from my_figures.four_by_two import vertical_top_cax
    from my_plot.init_ax import init_ts, init_dist
    from my_plot.legend import color_legend
    from my_plot.basic import plot, fill 
    from my_files.handy import save_df 

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

    df_doy_lc_mean_rmse         = column_wise(df_doy_lc_mean, ffunc = rmse)
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
    labels_sources              = {s: query_variables(s, 'name_label') for s in sources}

    cmapc                       = cc.glasbey_hv[:]
    colors                      = {labels_sources[k]: v for k,v in colors.items() if k in sources}
    colorsc                     = [cmapc[colors[d]] for d in colors.keys()]

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

def dist_landcover(name: str, 
                   df: pd.DataFrame, 
                   variable: str, 
                   sources_insitu: list[str], 
                   sources_grids: list[str], 
                   sel_landcover: list[str],
                   colors: dict = {}, 
                   dist_init_args: dict = {},
                   dist_args: dict = {},
                   color_legend_args: dict = {}):
    
    from my_series.group import select_multi_index, nona_level
    from my_series.aggregate import column_wise

    from my_math.stats import gauss_kde_pdf, pbias, rmse
    from my_resources.sources import query_variables

    from my_figures.two_by_two import square_top_cax
    from my_plot.init_ax import init_ts, init_dist
    from my_plot.legend import color_legend
    from my_plot.basic import plot, fill 
    from my_files.handy import save_df

    import colorcet as cc

    print('Plot land cover aggregated DOY and distribution plots...\n')
    
    df_nona                     = nona_level(df, ['Variable', 'Station'])

    df_s                        = select_multi_index(df_nona, ['Variable', 'Landcover'],
                                                      keys = [variable, sel_landcover])
    
    df_s                        = df_s.reindex(labels = sources_insitu + sources_grids, axis = 1, level = 'Source')

    sources                     = df_s.columns.unique(level = 'Source')

    df_dist_lc                  = df_s.groupby(axis = 1, level = ['Source', 'Landcover']).apply(gauss_kde_pdf, return_dict=True)

    df_dist_lc.columns          = df_dist_lc.columns.set_names('pdf', level = -1)

    all_xs                      = select_multi_index(df_dist_lc, 'pdf', 'xs')
    all_ys                      = select_multi_index(df_dist_lc, 'pdf', 'ys')

    var_units                   = query_variables(sources[0], 'var_units')[variable]
    labels_sources              = {s: query_variables(s, 'name_label') for s in sources}

    cmapc                       = cc.glasbey_hv[:]
    colors                      = {labels_sources[k]: v for k,v in colors.items() if k in sources}
    colorsc                     = [cmapc[colors[d]] for d in colors.keys()]

    fig, axs, axl               = square_top_cax(fy = 5.5)

    color_legend(axl, colors, cmapc, **color_legend_args)

    for ilc, lc in enumerate(sel_landcover):

        xs_dist                 = select_multi_index(df_dist_lc, levels = ['Landcover', 'pdf'], keys = [lc, 'xs'])

        ys_dist                 = select_multi_index(df_dist_lc, levels = ['Landcover', 'pdf'], keys = [lc, 'ys'])

        var_label               = f'{variable} [{var_units}]'

        init_dist(axs[ilc], all_xs, all_ys, xlabel = var_label, ax_tag = lc, **dist_init_args)

        plot(axs[ilc], xs_dist, ys_dist, colors = colorsc, **dist_args)

    return fig

def pie_landcover(df_static, selected_landcover, colors = {}, color_legend_args = {}):

    print('Plot network land cover pie plots\n')

    from my_series.aggregate import concat
    from my_resources.sources import query_static

    from my_figures.double import horizontal_top_cax
    from my_plot.basic import pie
    from my_plot.legend import color_legend

    from my_plot.init_ax import init_pie

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

    pie(axs[0], shares_lc, colorsc, autopct='%1.1f%%')
    pie(axs[1], shares_surf_o, colorsc_o, autopct='%1.1f%%')

    return fig


def doy_landcover(df, variable, sources_insitu, sources_grids, sel_landcover,
                       stat: str = 'mean', stat_err: str = 'std',
                       colors: dict = {}, doy_init_args = {},
                       doy_args = {}, doy_fill_args = {},
                       color_legend_args = {}, do_fill = False):
    
    print('Plot network land cover DOY plots\n')

    from my_series.group import select_multi_index, nona_level
    from my_resources.sources import query_variables

    from my_figures.two_by_two import square_top_cax
    from my_plot.init_ax import init_ts
    from my_plot.legend import color_legend
    from my_plot.basic import plot, fill 

    import colorcet as cc

    df_nona                     = nona_level(df, ['Variable', 'Station'])

    df_s                        = select_multi_index(df_nona, ['Variable', 'Landcover'],
                                                      keys = [variable, sel_landcover])
    
    df_s                        = df_s.reindex(labels = sources_insitu + sources_grids, axis = 1, level = 'Source')

    sources                     = df_s.columns.unique(level = 'Source')

    df_doy                      = df_s.groupby(df_s.index.dayofyear).mean()

    df_doy_lc                   = df_doy.groupby(axis = 1, level = ['Source', 'Landcover'])

    df_doy_lc_agg               = df_doy_lc.agg(stat)

    df_doy_lc_agg_err           = df_doy_lc.agg(stat_err)

    fig, axs, axl               = square_top_cax(fx = 8)

    var_units                   = query_variables(sources[0], 'var_units')[variable]
    labels_sources              = {s: query_variables(s, 'name_label') for s in sources}

    cmapc                       = cc.glasbey_hv[:]
    colors                      = {labels_sources[k]: v for k,v in colors.items() if k in sources}
    colorsc                     = [cmapc[colors[d]] for d in colors.keys()]

    color_legend(axl, colors, cmapc, **color_legend_args)

    for ilc, lc in enumerate(sel_landcover):

        xs_doy                  = df_doy_lc_agg.index

        ys_doy                  = select_multi_index(df_doy_lc_agg, levels = ['Landcover'], keys = [lc])
        
        err_doy                 = select_multi_index(df_doy_lc_agg_err, levels = ['Landcover'], keys = [lc])

        var_label               = f'{variable} [{var_units}]'

        lower                   = ys_doy - err_doy
        upper                   = ys_doy + err_doy

        init_ts(axs[ilc], xs_doy, df_doy_lc_agg, ylabel = var_label, ax_tag = lc, **doy_init_args)
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


def plot_ts_2(x, y, labels, variable, colors: dict = {}, color_legend_args: dict = {},
            fig_args: dict = {}, ts_init_args: dict = {}, plot_args: dict = {}):

    print(f'Plot station time-series: {variable}\n')

    from my_.figures.single import square_top_cax
    from my_.plot.init_ax import init_ts_2
    from my_.plot.basic import plot
    from my_.plot.legend import color_legend
    from my_.resources.sources import query_variables

    import colorcet as cc
    import numpy as np

    cmapc                       = cc.glasbey_hv[:]
    colors                      = {k: v for k, v in colors.items() if k in labels}
    colorsc                     = [cmapc[colors[d]] for d in list(labels)]

    fig, ax, axl                = square_top_cax(**fig_args)

    #var_units                   = query_variables('CLM5-EU3', 'var_units')[variable]

    if np.all(np.isnan(y)): return fig
    
    color_legend(axl, colors, cmapc, **color_legend_args)

    init_ts_2(ax, x, y, **ts_init_args)

    plot(ax, x, y, colors = colorsc, **plot_args)

    return  fig