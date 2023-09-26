

def single_EU3_point_locations(lats, lons, rotnpole_lat: float, rotnpole_lon: float, semmj_axis: int, semmn_axis: int,
                        lon_extents: list, lat_extents: list, lw_grid: float = 0.5, lw_coast: float = 0.5,  color_grid: str = 'gray',
                        ls_grid: str = '--', xticks: list = [], yticks: list = [], fs_label: float = 10, size_marker: float = 4.0, 
                        marker: str = 'x', color_marker: str = 'firebrick', alpha: float = 0.7, zorder: int = 5, title: str = ''):

    from my_.figures.single import square
    from my_.plot.style import style_1
    from my_.plot.maps import EU3_plot_init, EU3_plot_lines, map_point_locations

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
    from my_.figures.double import horizontal_cmap
    from my_.plot.basic import colormesh
    from my_.plot.maps import EU3_plot_init, EU3_plot_lines
    from my_.plot.colors import colormap, colorbar


    style_1()

    rp, pc, xs, ys              = EU3_plot_init(rotnpole_lat, rotnpole_lon, semmj_axis, semmn_axis, lon_extents, lat_extents)

    fig, axes, cax              = horizontal_cmap(projection = rp)

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
    from my_.figures.single import square_cmap
    from my_.plot.colors import colormap, colorbar
    from my_.plot.basic import colormesh

    import cartopy.feature as cfeature

    label_sides                 =  ['bottom', 'right']

    style_1()

    rp, pc, xs, ys              = EU3_plot_init(rotnpole_lat, rotnpole_lon, semmj_axis, semmn_axis, lon_extents, lat_extents)

    figure, ax, cax             = square_cmap(projection = rp)

    ax.add_feature(cfeature.OCEAN, edgecolor='face', facecolor='white', zorder = 2)

    cmap_n                      = np.max(array) + 1

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

    from my_.figures.two_by_two import square_two_top_legends
    from my_.series.group import select_multi_index, nona_level
    from my_.plot.basic import init_xy
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

    fig, axs, axs_l             = square_two_top_legends()

    colors                      = {k: v for k,v in colors.items() if k not in i_sources}

    marker_legend(axs_l[0], markers, **marker_legend_args)
    color_legend(axs_l[1], colors, cmapc, **color_legend_args)

    for iax, ax in enumerate(axs):

        agg_moment              = moments[iax]
        
        df_i_lc_agg             = df_i_lc.agg(agg_moment)
        df_d_lc_agg             = df_d_lc.agg(agg_moment)

        title_fig               = f'{variable} moments'

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

    