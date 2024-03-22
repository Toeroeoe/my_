import matplotlib as mpl
import matplotlib.pyplot as plt
import cartopy.crs as ccrs


def square(fx: float = 6.7, fy: float = 6.7, dpi: int = 300, projection = None, frame: bool = False):

    import matplotlib.pyplot as plt
    from my_plot.style import style_1

    style_1()

    fig                             = plt.figure(figsize=(fx, fy), dpi = dpi)

    ax                              = fig.add_subplot(111, projection = projection, frameon = frame)

    return fig, ax


def square_right_cax(fx: float = 6.7, fy: float = 6.7, dpi: int = 300, projection = None, frame: bool = False):

    import matplotlib.pyplot as plt
    from matplotlib.gridspec import GridSpec
    from my_plot.style import style_1
    
    style_1()
    
    nrows                           = 1
    ncols                           = 2
    w1, w2                          = 10, 1

    fig                             = plt.figure(figsize=(fx, fy), dpi = dpi, constrained_layout = True)

    gs                              = GridSpec(figure = fig, 
                                                ncols = ncols, nrows = nrows, 
                                                width_ratios = [w1, w2],
                                                wspace = 0.1)

    ax                              = fig.add_subplot(gs[0,0], projection = projection, frameon = frame)
    cax                             = fig.add_subplot(gs[0,1], frameon = frame)

    return fig, ax, cax


def square_top_cax(fx: float = 6.7, fy: float = 6.7, dpi: int = 300, projection = None, frame: bool = False):

    import matplotlib.pyplot as plt
    from matplotlib.gridspec import GridSpec
    from my_plot.style import style_1

    style_1()

    
    nrows                           = 2
    ncols                           = 1
    w1, w2                          = 1, 14

    fig                             = plt.figure(figsize=(fx, fy), dpi = dpi)

    gs                              = GridSpec(figure = fig, 
                                                ncols = ncols, nrows = nrows, 
                                                height_ratios = [w1, w2])
    
    ax                              = fig.add_subplot(gs[1,0], projection = projection, frameon = frame)
    cax                             = fig.add_subplot(gs[0,0], frameon = frame)

    return fig, ax, cax


def square_top_right_cax(fx: float = 6.7, 
                         fy: float = 6.7, 
                         dpi: int = 300, 
                         projection: None | ccrs.Projection = None, 
                         frame: bool = False):
    
    from matplotlib.gridspec import GridSpec
    from my_plot.style import style_1
    
    style_1()

    nrows                           = 2
    ncols                           = 2
    w1, w2                          = 1, 14
    h1, h2                          = 14, 1


    fig                             = plt.figure(figsize=(fx, fy), dpi = dpi)

    gs                              = GridSpec(figure = fig, 
                                                ncols = ncols, nrows = nrows, 
                                                height_ratios = [w1, w2],
                                                width_ratios = [h1, h2])
    
    ax                              = fig.add_subplot(gs[1,0], projection = projection, frameon = frame)
    caxt                            = fig.add_subplot(gs[0,0], frameon = frame)
    caxr                            = fig.add_subplot(gs[1,1], frameon = frame)

    return fig, ax, caxt, caxr