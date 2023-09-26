
def EU3_plot_init(rotnpole_lat: float = 39.25, rotnpole_lon: float = -162.0, semmj_axis: int = 6370000, 
                    semmn_axis: int = 6370000, lon_extents: list = [351.1, 60.55], lat_extents: list = [23.92, 66.1]):

    import numpy as np
    from cartopy import crs

    rp                          = crs.RotatedPole(pole_longitude = rotnpole_lon,
                                    pole_latitude = rotnpole_lat,
                                    globe = crs.Globe(semimajor_axis = semmj_axis,
                                    semiminor_axis = semmn_axis))
    
    pc                          = crs.PlateCarree()
    xs, ys, _                   = rp.transform_points(pc, np.array(lon_extents), np.array(lat_extents)).T
    
    return rp, pc, xs, ys


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
                        projection = None, zorder: int = 5, alpha: float = 0.8):

    import cartopy.feature as cfeature
    from my_.plot.basic import scatter

    ax.add_feature(cfeature.LAND, zorder = 0)
    ax.add_feature(cfeature.OCEAN, zorder = 0)

    artist = scatter(ax, lons, lats, sizes_marker = size_marker, marker = marker, colors_marker = color,
            projection = projection, alpha = alpha, zorder = zorder)

