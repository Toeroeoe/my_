
from dataclasses import dataclass, field
import matplotlib as mpl
import matplotlib.transforms as mtr
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import cartopy.crs as ccrs
from matplotlib.gridspec import GridSpec
import matplotlib.axes as maxes
from mpl_toolkits.axes_grid1 import make_axes_locatable
import string
import os
from pathlib import Path, PosixPath



@dataclass(kw_only = True)
class fig_001:

    fy: float = 6.7
    fx: float = 6.7

    dpi: int = 300
    font_color: str = 'dimgray'
    font_dir: Path = Path('/p/scratch/cjibg31/jibg3105/projects/my_py/src/my_/plot/fonts/')
    font: str = 'Montserrat-Medium'
    constrained: bool = True

    def create(self):
        
        font_files = fm.findSystemFonts(fontpaths = self.font_dir)
    
        for font_file in font_files:
            fm.fontManager.addfont(font_file)
    
        prop = fm.FontProperties(fname = PosixPath(str(self.font_dir) + 
                                         str(Path('/Montserrat-Medium.otf'))))

        mpl.rcParams['font.family'] = prop.get_name()
        mpl.rcParams['xtick.color'] = self.font_color
        mpl.rcParams['ytick.color'] = self.font_color

        fig_ = plt.figure(figsize = (self.fx, self.fy), 
                          constrained_layout = self.constrained,
                          dpi = self.dpi)
        
        self.fig = fig_
        
        return self

    def save(self, 
             path: os.PathLike,
             fformat: str = 'png'):

        self.fig.savefig(f'{path}.{fformat}',
                         dpi = self.dpi,
                         bbox_inches = 'tight')
        
        plt.close()

        

@dataclass(kw_only = True)
class single_001(fig_001):

    color_bar: None | list[str] = None
    projection: mtr.Transform | ccrs.Projection | None = None
    frame: bool = False
    aspect_factor: float = 12.0
    cax_pad: float = 0.8
    cax_size: str = '8%'


    def create(self):

        super().create()

        nrows = 1
        ncols = 1
        args = {'width_ratios': None,
                'height_ratios': None}
        axs = []
        caxs = []

        gs = GridSpec(figure = self.fig, 
                      ncols = ncols, 
                      nrows = nrows, 
                      **{k: v for k, v in args.items()
                         if v is not None})

        axs.append(self.fig.add_subplot(gs[0, 0], 
                                        projection = self.projection, 
                                        frameon = self.frame))
        

        if not self.color_bar: 

            self.caxs = None
        
        else:

            if 'right' in self.color_bar: 
                
                divider = make_axes_locatable(axs[0])

                caxs.append(divider.append_axes('right', 
                                                size = self.cax_size, 
                                                pad = self.cax_pad, 
                                                frameon = self.frame, 
                                                axes_class = maxes.Axes))

            if 'top' in self.color_bar: 
                
                divider = make_axes_locatable(axs[0])

                caxs.append(divider.append_axes('top', 
                                                size = self.cax_size, 
                                                pad = self.cax_pad, 
                                                frameon = self.frame, 
                                                axes_class = maxes.Axes))

        
        self.axs = axs
        self.caxs = caxs

        return self

    


@dataclass(kw_only = True)
class triple_001(fig_001):
    
    color_bar: None | list[str] = None
    projection: mtr.Transform | ccrs.Projection | None = None
    frame: bool = False
    aspect_factor: float = 12.0
    cax_pad: float = 0.8
    cax_size: str = '8%'


    def create(self):

        super().create()

        axs = []
        caxs = []

        nrows = 1
        ncols = 3

        args = {'width_ratios': None,
                'height_ratios': None}

        gs = GridSpec(figure = self.fig, 
                      nrows = nrows,
                      ncols = ncols,
                      **{k: v for k, v in args.items()
                         if v is not None})


        for iax in range(ncols):

            axs.append(self.fig.add_subplot(gs[0, iax], 
                                            projection = self.projection, 
                                            frameon = self.frame))
        

        if not self.color_bar: 

            self.caxs = None
        
        else:

            if 'right' in self.color_bar: 
                
                divider = make_axes_locatable(axs[-1])

                caxs.append(divider.append_axes('right', 
                                                size = self.cax_size, 
                                                pad = self.cax_pad, 
                                                frameon = self.frame, 
                                                axes_class = maxes.Axes))

        self.axs = axs
        self.caxs = caxs

        return self

        
    def annotation(self, 
                   x : float = 0.05, 
                   y : float = 1.05, 
                   fs: float = 12.0):

        abc = string.ascii_lowercase
    
        list_abc = list(abc)

        for iax, ax in enumerate(self.axs):

            ax.text(x, y, list_abc[iax] + ')', 
                    fontsize = fs,
                    transform = ax.transAxes, 
                    va = 'bottom', 
                    ha = 'center')         