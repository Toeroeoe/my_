

def axgrid(ax, color: str = 'dimgray', ls: str = '--', which: str = 'major', visible: bool = True, alpha: float = 0.4):

    ax.grid(which = which, color = color, visible = visible, ls = ls, alpha = alpha, zorder = 0)


def common_free_lims(ax, xs, ys, rel_b: float = 0.1):

    import numpy as np
    import pandas as pd

    if isinstance(ys, pd.Series): ys = ys.values
    if isinstance(xs, pd.Series): xs = xs.values

    imax                    = np.nanmax([*xs, *ys])
    imin                    = np.nanmin([*xs, *ys])

    max_rel                 = np.nanmax(np.abs([imax, imin]))

    imax_rel                = imax + max_rel * rel_b
    imin_rel                = imin - max_rel * rel_b

    ax.set_ylim((imin_rel, imax_rel))
    ax.set_xlim((imin_rel, imax_rel))

    return imin_rel, imax_rel


def bar_lims(ax, xs, ys, rel_b: float = 0.1):

    import numpy as np
    import pandas as pd

    if isinstance(ys, pd.Series): ys = ys.values
    if isinstance(xs, pd.Series): xs = xs.values

    xmax                    = np.max(xs)
    xmin                    = np.min(xs)

    ymax                    = np.max(ys)
    ymin                    = np.min(ys)

    xabs                    = np.max(np.abs([xmax, xmin]))
    yabs                    = np.max(np.abs([ymax, ymin]))

    xmax_rel                = xmax + xabs * rel_b + 0.5
    xmin_rel                = xmin - xabs * rel_b - 0.5

    ymax_rel                = ymax + yabs * rel_b
    ymin_rel                = 0 - yabs * rel_b

    ax.set_ylim((ymin_rel, ymax_rel))
    ax.set_xlim((xmin_rel, xmax_rel))

    return [xmin_rel, xmax_rel], [ymin_rel, ymax_rel]


def free_lims(ax, xs, ys, rel_b: float = 0.1):

    import numpy as np
    import pandas as pd

    if isinstance(ys, pd.Series): ys = ys.values
    if isinstance(ys, pd.DataFrame): ys = ys.values
    if isinstance(xs, pd.Series): xs = xs.values
    if isinstance(xs, pd.DataFrame): xs = xs.values

    xmax                    = np.nanmax(xs)
    xmin                    = np.nanmin(xs)

    ymax                    = np.nanmax(ys)
    ymin                    = np.nanmin(ys)

    xabs                    = np.nanmax(np.abs([xmax, xmin]))
    yabs                    = np.nanmax(np.abs([ymax, ymin]))

    xmax_rel                = xmax + xabs * rel_b + 0.5
    xmin_rel                = xmin - xabs * rel_b - 0.5

    ymax_rel                = ymax + yabs * rel_b
    ymin_rel                = ymin - yabs * rel_b

    ax.set_ylim((ymin_rel, ymax_rel))
    ax.set_xlim((xmin_rel, xmax_rel))

    return [xmin_rel, xmax_rel], [ymin_rel, ymax_rel]
    

def free_date_lim(ax, ts, x = True, y = False, rel_b: float = 0.1):

    import pandas as pd
    import numpy as np

    ts.dropna()

    tsmax                   = np.max(ts)
    tsmin                   = np.min(ts)

    if x: ax.set_xlim((tsmin, tsmax))
    if y: ax.set_ylim((tsmin, tsmax))

    return tsmin, tsmax


def free_numeric_lim(ax, xs, x = False, y = True, rel_b: float = 0.1):

    import pandas as pd
    import numpy as np

    if isinstance(xs, pd.Series): xs = xs.values
    if isinstance(xs, pd.DataFrame): xs = xs.values

    tsmax                   = np.nanmax(xs) 
    tsmin                   = np.nanmin(xs)

    tsabs                   = np.max(np.abs([tsmax, tsmin]))

    tsmax_rel               = tsmax + tsabs * rel_b + 0.5
    tsmin_rel               = tsmin - tsabs * rel_b - 0.5

    if x: ax.set_xlim((tsmin_rel, tsmax_rel))
    if y: ax.set_ylim((tsmin_rel, tsmax_rel))

    return tsmin_rel, tsmax_rel

    

def numeric_ticks(ax, nticks_y = 5, nticks_x = 5, fs_ticks = 10, integerx = False, integery = False,
                  x: bool = True, y: bool = True):

    from matplotlib.ticker import MaxNLocator

    xlocator                = MaxNLocator(prune = 'both', nbins = nticks_x, integer = integerx)
    ylocator                = MaxNLocator(prune = 'both', nbins = nticks_y, integer = integery)

    ax.yaxis.set_major_locator(ylocator)
    ax.xaxis.set_major_locator(xlocator)

    if not x: ax.set_xticklabels([])
    if not y: ax.set_yticklabels([])

    ax.tick_params(axis = 'both', which = 'major', labelsize = fs_ticks)
    

