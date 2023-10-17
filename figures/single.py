

def square(fx: float = 6.7, fy: float = 6.7, dpi: int = 300, projection = None, frame: bool = False):

    import matplotlib.pyplot as plt

    fig                             = plt.figure(figsize=(fx,fy), dpi= dpi)

    ax                              = fig.add_subplot(111, projection = projection, frameon = frame)

    return fig, ax


def square_right_cax(fx: float = 6.7, fy: float = 6.7, dpi: int = 300, projection = None, frame: bool = False):

    import matplotlib.pyplot as plt
    from matplotlib.gridspec import GridSpec
    
    nrows                           = 1
    ncols                           = 2
    w1, w2                          = 14, 1

    fig                             = plt.figure(figsize=(fx,fy), dpi= dpi)

    gs                              = GridSpec(figure = fig, 
                                                ncols = ncols, nrows = nrows, 
                                                width_ratios = [w1, w2], wspace = 0.3)

    ax                              = fig.add_subplot(gs[0,0], projection = projection, frameon = frame)
    cax                             = fig.add_subplot(gs[0,1], frameon = frame)

    return fig, ax, cax