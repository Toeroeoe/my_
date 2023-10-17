

def axgrid(ax, ls: str = '--', which: str = 'major', visible: bool = True, alpha: float = 0.5):

    ax.grid(which = which, visible = visible, ls = ls, alpha = alpha, zorder = 0)


def common_free_lims(ax, xs, ys, rel_b: float = 0.1):

    import numpy as np
    import pandas as pd

    if isinstance(ys, pd.Series): ys = ys.values
    if isinstance(xs, pd.Series): xs = xs.values

    imax                    = np.max([*xs, *ys])
    imin                    = np.min([*xs, *ys])

    if imax > 0:

        abs_rel_b           = rel_b * imax

    if imax <= 0:

        abs_rel_b           = abs(rel_b * imin)

    imax_rel                = imax + abs_rel_b
    imin_rel                = imin - abs_rel_b

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

    xmax                    = np.max(xs)
    xmin                    = np.min(xs)

    ymax                    = np.max(ys)
    ymin                    = np.min(ys)

    xabs                    = np.max(np.abs([xmax, xmin]))
    yabs                    = np.max(np.abs([ymax, ymin]))

    xmax_rel                = xmax + xabs * rel_b + 0.5
    xmin_rel                = xmin - xabs * rel_b - 0.5

    ymax_rel                = ymax + yabs * rel_b
    ymin_rel                = ymin - yabs * rel_b

    ax.set_ylim((ymin_rel, ymax_rel))
    ax.set_xlim((xmin_rel, xmax_rel))

    return [xmin_rel, xmax_rel], [ymin_rel, ymax_rel]
    


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
    

