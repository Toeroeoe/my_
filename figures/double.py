

def horizontal(fx: float = 6.7, fy: float = 3.35, dpi: int = 300, projection = None, frame: bool = False):

    import matplotlib.pyplot as plt

    nrows                           = 1
    ncols                           = 2

    fig                             = plt.figure(figsize=(fx,fy), dpi= dpi)

    ax1                             = fig.add_subplot(nrows, ncols, 1, projection = projection, frameon = frame)
    ax2                             = fig.add_subplot(nrows, ncols, 2, projection = projection, frameon = frame)

    return fig, [ax1, ax2]


def horizontal_cmap(fx: float = 6.7, fy: float =3.35, dpi: int = 300, projection = None, frame: bool = False):

    import matplotlib.pyplot as plt
    from matplotlib.gridspec import GridSpec

    nrows                           = 1
    ncols                           = 3
    w1, w2                          = 14, 1

    fig                             = plt.figure(figsize=(fx,fy), dpi= dpi)

    gs                              = GridSpec(figure = fig, 
                                                ncols = ncols, nrows = nrows, 
                                                width_ratios = [w1, w1, w2], wspace = 0.3)

    ax1                             = fig.add_subplot(gs[0, 0], projection = projection, frameon = frame)
    ax2                             = fig.add_subplot(gs[0, 1], projection = projection, frameon = frame)

    cax                             = fig.add_subplot(gs[0, 2], frameon = frame)

    return fig, [ax1, ax2], cax