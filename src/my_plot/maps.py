

def EU3_plot_lines(ax, pc, xs, ys, 
                    lw_grid: float = 0.5, lw_coast: float = 0.5, color_grid: str = 'grey', 
                    ls_grid: str = '--', xticks = [], yticks = [],
                    fs_label: float = 8, label_sides: list = ['bottom', 'right']):
    
    import matplotlib.ticker as mticker

    ax.coastlines(linewidth = lw_coast, zorder=2)
    
    gl                          = ax.gridlines(crs = pc, 
                                                linewidth = lw_grid,
                                                color = color_grid, 
                                                linestyle = ls_grid, 
                                                draw_labels = True, 
                                                x_inline = False, 
                                                y_inline = False, 
                                                zorder = 3)
    if 'right' not in label_sides: 
        gl.right_labels         = False
    if 'bottom' not in label_sides:
        gl.bottom_labels        = False
    if 'top' not in label_sides:
        gl.top_labels           = False
    if 'left' not in label_sides:
        gl.left_labels          = False
    
    gl.xlocator                 = mticker.FixedLocator(xticks)
    gl.ylocator                 = mticker.FixedLocator(yticks)
    gl.xlabel_style             = {'size': fs_label}
    gl.ylabel_style             = {'size': fs_label}

    ax.set_extent([*xs,*ys])


def map_point_locations(ax, lats = [], lons = [], 
                        size_marker: list = [], marker: str = 'x', color: list = [], 
                        projection = None, zorder: int = 5, alpha: float = 0.8,
                        alpha_land = 1.0, alpha_ocean = 0.3, land_color = 'dimgrey', ocean_color = None):

    import cartopy.feature as cfeature
    from my_plot.basic import scatter

    ax.add_feature(cfeature.LAND, color = land_color, alpha = alpha_land, zorder = 0)
    ax.add_feature(cfeature.OCEAN, color= ocean_color, alpha = alpha_ocean, zorder = 0)

    artist = scatter(ax, lons, lats, sizes_marker = size_marker, marker = marker, colors_marker = color,
            projection = projection, alpha = alpha, zorder = zorder)

    return artist