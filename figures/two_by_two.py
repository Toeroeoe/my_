

def square_two_top_legends(fx: float = 6.7, fy: float = 6.7, dpi: int = 300, 
                        layout: str = 'constrained', projection = None, frame: bool = False,
                        hspace: float = 0.05, wspace: float = 0.05):

    import matplotlib.pyplot as plt
    from matplotlib.gridspec import GridSpec

    from my_.plot.style import style_1

    style_1()

    ncols, nrows                    = 2, 3

    figure                          = plt.figure(figsize = (fx, fy), dpi = dpi, layout = layout)

    gs                              = GridSpec(figure = figure, ncols = ncols, nrows = nrows,
                                               height_ratios = [1, 20, 20],
                                               hspace = hspace, wspace = wspace)

    axs_kw                          = {'frameon': frame, 'projection': projection}

    axs                             = gs.subplots(subplot_kw = axs_kw).flatten()

    return figure, axs[2:], axs[0:2]




