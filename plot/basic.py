

def colormesh(ax, x, y, array, cmap: str = 'coolwarm_r', v0: float = None, v1: float = None, projection = None):

    artist = ax.pcolormesh(x, y, array, cmap = cmap, vmin = v0, vmax = v1, transform = projection, zorder=0)
    
    return artist


def scatter(ax, xs, ys, marker = None, sizes_marker: int = 50, colors_marker: str = 'black', 
            alpha: float = 0.7, projection = None, zorder: int = 5):

    if isinstance(sizes_marker, int): sizes_marker = [sizes_marker] * len(xs)
    if isinstance(colors_marker, str): colors_marker = [colors_marker] * len(xs)

    if projection == None: projection = ax.transData

    artist = ax.scatter(xs, ys, marker = marker, s = sizes_marker, c = colors_marker, 
                        alpha = alpha, transform = projection, zorder = zorder)

    return artist


def xy(ax, xs, ys, marker, sizes_marker = 50, colors_marker = [], projection = None, 
       axhv_color: str = 'k', axhv_ls: str = '--', axhv_lw: float = 0.7, axhv_alpha: float = 0.8, axhv_dashes: tuple = (4, 4),
       diag_color: str = 'k', diag_ls: str = '--', diag_lw: float = 0.7, diag_alpha: float = 0.8, diag_dashes = (4,4),
       xlabel: str = '', ylabel: str = '', fs_label: int = 9):

    from my_.plot.basic import scatter
    
    init_xy(ax, xs, ys, axhv_color, axhv_ls, axhv_lw, axhv_alpha, axhv_dashes,
       diag_color, diag_ls, diag_lw, diag_alpha, diag_dashes, xlabel, ylabel, fs_label)

    artist = scatter(ax, xs, ys, marker = marker, sizes_markers = sizes_marker, colors_markers = colors_marker, projection = projection)

    return artist


def init_xy(ax, xs, ys, axhv_color: str = 'k', axhv_ls: str = '--', axhv_lw: float = 0.7, axhv_alpha: float = 0.8, axhv_dashes: tuple = (4, 4),
       diag_color: str = 'k', diag_ls: str = '--', diag_lw: float = 0.7, diag_alpha: float = 0.8, diag_dashes = (4,4),
       title: str = '', xlabel: str = '', ylabel: str = '', y_title: float = 1.1, fs_title: int = 14, fs_label: int = 12, fs_ticks = 10,
       ax_tag = '', ax_tag_x: float = 0.5, ax_tag_y: float = 1.0):
    
    from my_.plot.limits import axgrid, xy_lims, xy_ticks
    from my_.plot.style import nospines

    import matplotlib.pyplot as plt

    
    axgrid(ax)
    nospines(ax)
    ax.axis('equal')

    plt.suptitle(title, fontsize = fs_title, y = y_title)
    
    ax.set_ylabel(ylabel, fontsize = fs_label)
    ax.set_xlabel(xlabel, fontsize = fs_label)
    
    ax.tick_params(axis='both', which='major', pad=10)

    ax.axhline(0, color = axhv_color, 
                ls = axhv_ls, lw = axhv_lw, 
                alpha = axhv_alpha, dashes = axhv_dashes, zorder = 0)
    
    ax.axvline(0, color = axhv_color, 
                ls = axhv_ls, lw = axhv_lw, 
                alpha = axhv_alpha, dashes = axhv_dashes, zorder = 0)

    ax.plot([-1.1, 1.1], [-1.1, 1.1], 
            transform = ax.transAxes, color = diag_color, 
            ls = diag_ls, lw = diag_lw, 
            alpha = diag_alpha, dashes = diag_dashes, zorder = 0)
    
    imin, imax = xy_lims(ax, xs, ys)

    xy_ticks(ax, imin, imax, fs_ticks = fs_ticks)

    props = dict(facecolor='white', edgecolor='none', alpha=0.85)

    ax.text(ax_tag_x, ax_tag_y, ax_tag, fontsize = fs_label, transform=ax.transAxes, va='bottom', ha='center', bbox=props)


