
import matplotlib.pyplot as plt
from matplotlib.cm import ScalarMappable

def marker_legend(ax, dict_labels_markers, marker_color = 'grey', marker_size = 10, labelcolor = 'k',
                  anchor = (0.5, 0), markerfirst = True, fs_labels = 12, handletextpad: float = 0.2,
                  columnspacing: float = 0.9, loc = 'lower center', handlelength: float = 1.2):

    from matplotlib.lines import Line2D
    
    ax.set_yticks([])
    ax.set_xticks([])

    handles                     = [Line2D([0], [0], marker = dict_labels_markers[ll], 
                                     color = 'white', markeredgecolor = marker_color, 
                                      markersize = marker_size, label = ll) for ll in dict_labels_markers]
    
    labels                      = list(dict_labels_markers.keys())

    ax.legend(handles, labels, fontsize = fs_labels, ncol = len(handles), frameon = False, labelcolor = labelcolor,
            loc = loc, bbox_to_anchor = anchor, handletextpad = handletextpad, columnspacing = columnspacing,
            handlelength = handlelength, bbox_transform = ax.transAxes, markerfirst = markerfirst)
    

def color_legend(ax: plt.axes,
                 dict_labels_colors: dict,
                 cmap: ScalarMappable | list,
                 linewidth: float = 5.0, 
                 fs_labels: float = 10.0,
                 anchor: tuple = (0.5, 0), 
                 markerfirst: bool = True,
                 handletextpad: float = 0.35,
                 columnspacing: float = 0.9, 
                 loc: str = 'lower center', 
                 handlelength: float = 1.0,
                 nrows: int = 1):

    from matplotlib.lines import Line2D
    
    ax.set_yticks([])
    ax.set_xticks([])

    handles                     = [Line2D([0], [0], color = cmap[v],
                                        linewidth = linewidth, label = k) 
                                        for k, v in dict_labels_colors.items()]
    
    ncol                        = len(handles) / nrows

    labels                      = list(dict_labels_colors.keys())

    short_labels                = [l.replace('-EU3', '') for l in labels]

    ax.legend(handles, short_labels, 
            fontsize = fs_labels, 
            ncol = ncol, 
            frameon = False, 
            loc = loc, 
            bbox_to_anchor = anchor, 
            handletextpad = handletextpad, 
            columnspacing = columnspacing,
            handlelength = handlelength, 
            bbox_transform = ax.transAxes, 
            markerfirst = markerfirst)