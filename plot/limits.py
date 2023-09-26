

def axgrid(ax, ls: str = '--', which: str = 'major', visible: bool = True, alpha: float = 0.5):

    ax.grid(which = which, visible = visible, ls = ls, alpha = alpha, zorder = 0)


def xy_lims(ax, xs, ys, rel_b: float = 0.1):

    imax                    = max(*xs,*ys)
    imin                    = min(*xs,*ys)

    imax_rel                = imax * (1 + rel_b)
    imin_rel                = imin * (1 - rel_b)

    ax.set_ylim((imin_rel, imax_rel))
    ax.set_xlim((imin_rel, imax_rel))

    return imin_rel, imax_rel


def xy_ticks(ax, imin, imax, nticks = 5, decimals = 2, fs_ticks = 10):

    import numpy as np

    floor                   = np.floor(imin)

    ceil                    = np.ceil(imax)

    linspace                = np.linspace(floor, ceil, nticks)

    ticks                   = np.round(linspace, decimals)
    
    ax.set_xticks(ticks, fontsize = fs_ticks)
    ax.set_yticks(ticks, fontsize = fs_ticks)

