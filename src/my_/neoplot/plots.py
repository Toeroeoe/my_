import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from dataclasses import dataclass, field
from matplotlib.ticker import MaxNLocator
import matplotlib.dates as mdates
import matplotlib.transforms as mtr
from cartopy.mpl.geoaxes import GeoAxes
import cartopy.crs as ccrs
import cartopy.feature as cfeature

from typing import Literal

@dataclass(kw_only = True)
class base_001:

    ax: plt.Axes

    grid: bool = True 
    grid_which: Literal['major', 'minor', 'both'] = 'major'
    grid_color: str = 'dimgray'
    grid_ls: str = '--'
    grid_alpha: float = 0.8
    tick_pad: float = 10.0

    no_spines: None | list[str] = field(default_factory = 
                                        lambda: ['top', 
                                                 'right', 
                                                 'bottom', 
                                                 'left'])

    y_title: float = 1.1 
    fs_title: int = 14 
    title: str = '' 

    axis: bool = False
    axis_color: str = 'k' 
    axis_ls: str = '--' 
    axis_lw: float = 0.7 
    axis_alpha: float = 0.8 
    axis_dashes: tuple = (4, 4)

    xlabel: str = '' 
    ylabel: str = '' 

    fs_label: float = 12.0
    ax_tag: str = ''
    ax_tag_x: float = 0.5
    ax_tag_y: float = 1.0 


    def decoration(self):
        
        if self.grid:
        
            self.ax.grid(which = self.grid_which, 
                         color = self.grid_color, 
                         visible = True, 
                         ls = self.grid_ls, 
                         alpha = self.grid_alpha, 
                         zorder = 0)


        if self.no_spines is not None:
            for spine in self.no_spines:
                    self.ax.spines[spine].set_visible(False)
            
        self.ax.set_title(self.title, 
                          fontsize = self.fs_title, 
                          y = self.y_title)
        
        self.ax.set_ylabel(self.ylabel, 
                           fontsize = self.fs_label)
        
        self.ax.set_xlabel(self.xlabel, 
                           fontsize = self.fs_label)

        self.ax.tick_params(axis = 'both', 
                            which = 'major', 
                            pad = self.tick_pad)
        
        if self.axis:

            self.ax.axline((0, 0), (0, 1),
                           color = self.axis_color, 
                           ls = self.axis_ls, 
                           lw = self.axis_lw, 
                           alpha = self.axis_alpha, 
                           dashes = self.axis_dashes,
                           transform = self.ax.transAxes, 
                           zorder = 0)

            self.ax.axline((0, 0), (1, 0),
                           color = self.axis_color, 
                           ls = self.axis_ls, 
                           lw = self.axis_lw, 
                           alpha = self.axis_alpha, 
                           dashes = self.axis_dashes, 
                           transform = self.ax.transAxes,
                           zorder = 0)
        
        props = dict(facecolor = 'white', 
                     edgecolor = 'none', 
                     alpha = 0.85)

        self.ax.text(self.ax_tag_x, 
                     self.ax_tag_y, 
                     self.ax_tag, 
                     fontsize = self.fs_label, 
                     transform = self.ax.transAxes, 
                     va = 'bottom', 
                     ha = 'center',
                     bbox = props)


@dataclass(kw_only = True)
class time_series(base_001):
    
    xs: np.ndarray | pd.DatetimeIndex
    ys: np.ndarray | pd.Series

    fs_ticks: float = 10.0
    ticks_y: bool = True
    ticks_x: bool = True
    nticks_y: int = 5
    nticks_x: int = 5
    integery: bool = False

    date_limits: None | list[np.datetime64] = None
    y_limits: None | list[float] = None
    y_ticks_rel_b: float = 0.1
    x_ticks_rel_b: float = 0.1

    def ticks(self):

        xlocator = mdates.AutoDateLocator(minticks = self.nticks_x)
        ylocator = MaxNLocator(prune = 'both', 
                               nbins = self.nticks_y, 
                               integer = self.integery)
    
        self.ax.xaxis.set_major_formatter(mdates.AutoDateFormatter(xlocator))

        self.ax.yaxis.set_major_locator(ylocator)
        self.ax.xaxis.set_major_locator(xlocator)

        if not self.ticks_x: self.ax.set_xticklabels([])
        if not self.ticks_y: self.ax.set_yticklabels([])

        self.ax.tick_params(axis = 'both', 
                            which = 'major', 
                            labelsize = self.fs_ticks)


    def limits(self):

        if self.date_limits is None:
        
            tsmax = np.max(self.xs)
            tsmin = np.min(self.xs)


            rel_d = (tsmax - tsmin).days * self.x_ticks_rel_b

            rel_dd = pd.Timedelta(rel_d, 'D')

            self.ax.set_xlim(tsmin - rel_dd, tsmax + rel_dd)
        
        else:

            for id, date in enumerate(self.date_limits):

                if isinstance(date, str):

                    self.date_limits[id] = pd.to_datetime(date).to_datetime64()

            self.ax.set_xlim(self.date_limits[0], 
                             self.date_limits[1])

            
        if self.y_limits is None:
            
            tsmax = np.nanmax(self.ys) 
            tsmin = np.nanmin(self.ys)

            tsabs = np.max(np.abs([tsmax, tsmin]))

            tsmax_rel = tsmax + tsabs * self.y_ticks_rel_b
            tsmin_rel = tsmin - tsabs * self.y_ticks_rel_b

            self.ax.set_ylim(tsmin_rel, tsmax_rel)

        else:

            self.ax.set_ylim(self.y_limits[0], 
                             self.y_limits[1])
            
    
    def create(self):

        super().decoration()
        
        self.ticks()
        self.limits()

        return self

        
    def plot(self,
             xs: np.ndarray | pd.DatetimeIndex,
             ys: np.ndarray | pd.Series,
             colors: str | list[str] = 'k',
             style: str | list[str] = '',
             lw: float | list[float] = 1.0,
             alpha: float = 0.8,
             projection: None | mtr.Transform | ccrs.Projection = None,
             markersize: float = 3.0,
             marker: str | list[str] = 'o',
             fillstyle: str = 'full',
             zorder: int = 5):

        ys = np.stack([y.flatten() for y in ys], axis = 1)
        
        if projection is None: 
            projection = self.ax.transData

        if isinstance(colors, str):
            colors = [colors]
        
        if isinstance(style, str):
            style = [style]
        
        if isinstance(marker, str):
            marker = [marker] 
            
        if isinstance(lw, int) or isinstance(lw, float):
            lw = [lw]

        self.ax.set_prop_cycle(color = colors,
                               linestyle = style,
                               marker = marker,
                               linewidth = lw)

        self.ax.plot(xs, 
                     ys,
                     transform = projection, 
                     markersize = markersize,
                     fillstyle = fillstyle,
                     alpha = alpha, 
                     zorder = zorder)



@dataclass(kw_only = True)
class amap(base_001):
    
    ax: GeoAxes
    lon: np.ndarray
    lat: np.ndarray

    grid: bool = False

    lon_extents: list[float] = field(default_factory =
                                    lambda: [-180.0, 180.0])
    lat_extents: list[float] = field(default_factory =
                                     lambda: [-90, 90])

    semmj_axis: None | int = 6370000
    semmn_axis: None | int = 6370000 

    fs_ticks: float = 10.0
    ticks_y: bool = True
    ticks_x: bool = True
    nticks_y: int = 4
    nticks_x: int = 4
    integery: bool = True
    integerx: bool = True
    
    feature_land: bool = False
    feature_ocean: bool = False
    
    land_alpha: float = 0.7
    ocean_alpha: float = 0.7
    land_color: str = 'gray'
    ocean_color: str = 'steelblue'
    lw_coast: float = 0.8
    lw_lines: float = 0.8
    color_lines: str = 'grey'
    ls_lines: str = '--'
    label_lines: list[str] = field(default_factory = 
                                        lambda: ['right', 
                                                 'bottom'])

    projection: ccrs.Projection = ccrs.PlateCarree()

    def features(self):

        if self.feature_ocean:
            self.ax.add_feature(cfeature.OCEAN,
                                color = self.ocean_color, 
                                alpha = self.ocean_alpha, 
                                zorder = 0)
            
        if self.feature_land:
            self.ax.add_feature(cfeature.LAND,
                                color = self.land_color, 
                                alpha = self.land_alpha, 
                                zorder = 0)
            
        self.ax.coastlines(linewidth = self.lw_coast, zorder=2)
            
    def limits(self):

            self.ax.set_extent([*self.lon_extents,
                                *self.lat_extents])
            
    
    def lines(self):
        
        gl = self.ax.gridlines(crs = self.projection, 
                               linewidth = self.lw_lines,
                               color = self.color_lines, 
                               linestyle = self.ls_lines, 
                               draw_labels = True, 
                               x_inline = False, 
                               y_inline = False, 
                               zorder = 5)


        for side in ['right', 'left', 'bottom', 'top']:

            if side not in self.label_lines:
                
                sideattr = getattr(gl, f'{side}_labels')
                sideattr = False

        self.grid_lines = gl

    def ticks(self):

        ylocator = MaxNLocator(prune = 'both', 
                               nbins = self.nticks_y, 
                               integer = self.integery)
        
        xlocator = MaxNLocator(prune = 'both', 
                               nbins = self.nticks_x, 
                               integer = self.integerx)
        
        self.ax.yaxis.set_major_locator(ylocator)
        self.ax.xaxis.set_major_locator(xlocator)

        self.grid_lines.xlabel_style = {'size': self.fs_ticks}
        self.grid_lines.ylabel_style = {'size': self.fs_ticks}

    
    def create(self):

        super().decoration()
        
        self.features()
        self.limits()
        self.ticks()
        self.lines()

        return self

    

@dataclass(kw_only = True)
class EU_CORDEX(amap):

    lon_extents: list[float] = field(default_factory =
                                    lambda: [351.1, 57])
    lat_extents: list[float] = field(default_factory =
                                     lambda: [27, 65.7])
    
    rotnpole_lat: float = 39.25 
    rotnpole_lon: float = -162.0

    def __post_init__(self):

        globe = ccrs.Globe(semimajor_axis = self.semmj_axis,
                           semiminor_axis = self.semmn_axis)

        self.rp = ccrs.RotatedPole(pole_longitude = self.rotnpole_lon,
                                   pole_latitude = self.rotnpole_lat,
                                   globe = globe)
        
        self.lon_extents, self.lat_extents, _ = \
                        self.rp.transform_points(self.projection, 
                                                 np.array(self.lon_extents), 
                                                 np.array(self.lat_extents)).T

        
