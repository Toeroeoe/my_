import numpy as np
import xarray as xr
from cartopy.crs import Projection
from my_.plot.basic import plot
           

regions = {'BI': [(-10, 50), (2, 50), (2, 59), (-10, 59)],
           'IP': [(-10, 36), (3, 36), (3,44), (-10, 44)],
           'FR': [(-5, 44), (5, 44), (5, 50), (-5, 50)],
           'ME': [(2, 48), (16, 48), (16, 55), (2, 55)],
           'SC': [(5, 55), (30, 55), (30, 70), (5, 70)],
           'AL': [(5, 44), (15, 44), (15, 48), (5, 48)],
           'MD': [(3, 36), (25, 36), (25, 44), (3, 44)],
           'EA': [(16, 44), (30, 44), (30, 55), (16, 55)],}


def plot_regions(ax, 
                    color: str = 'k',
                    lw: float = 1.3,
                    projection: None | Projection = None,
                    alpha: float = 0.8):
    
    for reg, points in regions.items():
        
        for i, v in enumerate(points):

            next = i + 1 if i < 3 else 0
        
            lats = np.linspace(points[i][1], points[next][1], 1000)
            lons = np.linspace(points[i][0], points[next][0], 1000)

            plot(ax, lons, lats,
                    colors = color,
                    lw = lw,
                    projection = projection,
                    alpha = alpha)


def mask_prudence(array: np.ndarray | xr.DataArray,
                  lat: np.ndarray | xr.DataArray,
                  lon: np.ndarray | xr.DataArray,
                  sel_regions: str | list[str] | None):
    
    
    #if isinstance(array, np.ndarray): 

    if sel_regions is None: return array

    shape = array.shape

    #mask = np.zeros(shape[-2:])

    for r in sel_regions:

        points = regions[r]
        
        if isinstance(array, xr.DataArray): 
            
            array = array.where(lat >= points[0][1])
            array = array.where(lat <= points[2][1])
            array = array.where(lon >= points[0][0])
            array = array.where(lon <= points[2][0])

    #array_masked = array.where(mask)
    #print(np.count_nonzero(~np.isnan(array)))
    #print(np.count_nonzero(~np.isnan(array_masked)))

    return array