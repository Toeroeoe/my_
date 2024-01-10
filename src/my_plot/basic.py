

def colormesh(ax, x, y, array, cmap: str = 'coolwarm_r', v0: float = None, v1: float = None, projection = None):

    artist = ax.pcolormesh(x, y, array, cmap = cmap, vmin = v0, vmax = v1, transform = projection, zorder=0)
    
    return artist


def scatter(ax, xs, ys, marker = None, sizes_marker: int = 50, colors_marker: str = 'black', 
            face: bool = True, alpha: float = 0.7, projection = None, zorder: int = 5):

    if isinstance(sizes_marker, int): sizes_marker = [sizes_marker] * len(xs)
    if isinstance(colors_marker, str): colors_marker = [colors_marker] * len(xs)

    if projection == None: projection = ax.transData

    artist = ax.scatter(xs, ys, marker = marker, s = sizes_marker, c = colors_marker,
                        alpha = alpha, transform = projection, zorder = zorder)
    
    if not face: artist.set_facecolor("none")

    return artist


def xy(ax, xs, ys, marker, sizes_marker = 50, colors_marker = [], projection = None, 
       axhv_color: str = 'k', axhv_ls: str = '--', axhv_lw: float = 0.7, axhv_alpha: float = 0.8, axhv_dashes: tuple = (4, 4),
       diag_color: str = 'k', diag_ls: str = '--', diag_lw: float = 0.7, diag_alpha: float = 0.8, diag_dashes = (4,4),
       xlabel: str = '', ylabel: str = '', fs_label: int = 9):

    from my_plot.basic import scatter
    from my_plot.init_ax import init_xy
    
    init_xy(ax, xs, ys, axhv_color, axhv_ls, axhv_lw, axhv_alpha, axhv_dashes,
       diag_color, diag_ls, diag_lw, diag_alpha, diag_dashes, xlabel, ylabel, fs_label)

    artist = scatter(ax, xs, ys, marker = marker, sizes_markers = sizes_marker, colors_markers = colors_marker, projection = projection)

    return artist


def bar(ax, xs, ys, color, width: float = 0.8, alpha: float = 0.8):

    artist = ax.bar(xs, ys, color = color, width = width, alpha = alpha, zorder = 5)

    return artist


def plot(ax, xs, ys, colors, style: str = '-', lw: float = 1.0, alpha: float = 0.8,
        markersize: float = 1.0, marker: str = '', zorder = 5):

    if isinstance(colors, list): ax.set_prop_cycle('color', colors)

    artist = ax.plot(xs, ys, ls = style, lw = lw, marker = marker, markersize = markersize, alpha = alpha, zorder = zorder)

    return artist


def fill(ax, xs, y1s, y2s, colors, alpha: float = 0.4, zorder: int = 2):

    if (y1s.ndim == 2):

        for iy, y1 in enumerate(y1s):
            
            artist = ax.fill_between(xs, y1s[y1], y2s.iloc[:,iy], color = colors[iy], alpha = alpha, zorder = zorder)

    return artist


def pie(ax, shares, colors):

    ax.pie(shares, colors = colors)