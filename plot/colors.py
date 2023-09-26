

def colorbar(cax, artist, ylabel: str = '', pad: int = 10, extend = 'neither', fs_label: float = 10, tick_labels = []):

    import matplotlib.pyplot as plt
    import numpy as np
    
    cbar = plt.colorbar(artist, cax = cax, extend = extend)

    cbar.ax.set_ylabel(ylabel, labelpad = pad, rotation = 270, fontsize = fs_label)

    len_tick_labels         = len(tick_labels)

    if len_tick_labels > 0:

        positions           = np.linspace(0.5, (len_tick_labels - 1) - 0.5, len_tick_labels)
        
        cbar.ax.set_yticks(positions, tick_labels)


def colormap(cmap: str = 'viridis', cmap_n = 1000):

    import matplotlib.pyplot as plt


    cmap_c                  = plt.cm.get_cmap(cmap, cmap_n)

    return cmap_c