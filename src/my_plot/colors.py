

def colorbar(cax, artist, ylabel: str = '', pad: int = 10, extend = 'neither', fs_label: float = 10, tick_labels = []):

    import matplotlib.pyplot as plt
    import numpy as np
    
    cbar = plt.colorbar(artist, cax = cax, extend = extend)

    cbar.ax.set_ylabel(ylabel, labelpad = pad, rotation = 270, fontsize = fs_label)

    len_tick_labels         = len(tick_labels)

    if len_tick_labels > 0:

        positions           = np.linspace(0.5, (len_tick_labels - 1) - 0.5, len_tick_labels)
        
        cbar.ax.set_yticks(positions, tick_labels, fontsize = fs_label)


def colormap(cmap: str = 'viridis', cmap_n = 1000):

    import matplotlib.pyplot as plt


    cmap_c                  = plt.cm.get_cmap(cmap, cmap_n)

    return cmap_c


def truncate_colormap(cmap, minval=0.0, maxval=1.0, n=100):
  
    import matplotlib.colors as colors
    import numpy as np
  
    new_cmap = colors.LinearSegmentedColormap.from_list(
        'trunc({n},{a:.2f},{b:.2f})'.format(n=cmap.name, a=minval, b=maxval),
        cmap(np.linspace(minval, maxval, n)))
    
    return new_cmap   