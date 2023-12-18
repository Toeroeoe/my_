

def marker_legend(ax, dict_labels_markers, marker_color = 'grey', marker_size = 10, labelcolor = 'k',
                  anchor = (0.5, 0), markerfirst = True, fs_labels = 10, handletextpad: float = 0.2,
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
    

def color_legend(ax, dict_labels_colors, cmap, linewidth: float = 5, fs_labels: float = 10,
                anchor = (0.5, 0), markerfirst = True, handletextpad: float = 0.35,
                columnspacing: float = 0.9, loc = 'lower center', handlelength: float = 1.0,
                nrows: int = 1):

    from matplotlib.lines import Line2D
    
    ax.set_yticks([])
    ax.set_xticks([])

    handles                     = [Line2D([0], [0], color = cmap[dict_labels_colors[ll]],
                                linewidth = linewidth, label = ll) for ll in dict_labels_colors]
    
    ncol                        = int(1 + (len(handles) / nrows))

    labels                      = list(dict_labels_colors.keys())

    short_labels                = [l.replace('-EU3', '') for l in labels]

    ax.legend(handles, short_labels, fontsize = fs_labels, ncol = ncol, frameon = False, 
            loc = loc, bbox_to_anchor = anchor, handletextpad = handletextpad, columnspacing = columnspacing,
            handlelength = handlelength, bbox_transform = ax.transAxes, markerfirst = markerfirst)