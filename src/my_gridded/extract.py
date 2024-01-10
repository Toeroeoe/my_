
"""
A python script to extract netcdf grid-cell data from any grid
Stations information in csv file
The out put time series can be in parquet or csv
"""

def closest_cells(coords_points, coords_cells, shape):

    import numpy as np

    cells = [closest_cell(coords_points[i], coords_cells, shape)[0] for i in range(len(coords_points))]

    return np.array(cells)



def closest_cell(coords_point, coords_cells, shape):
    
    """
    Find the closest coordinate point.
    Given a point in 2d coordinates,
    and a list of points find the node.
    """


    import numpy as np

    coords_point    = coords_point if isinstance(coords_point, np.ndarray) else np.array(coords_point)
   
    deltas          = np.subtract(coords_cells, coords_point)

    # Sum the lat and lon differences of each cell
    dist            = np.einsum('ij,ij->i', deltas, deltas)

    closest_i       = np.nanargmin(dist)

    closest_coords  = coords_cells[closest_i, :]

    closest_cell    = np.unravel_index(closest_i, shape)

    return closest_cell, closest_coords


def grid_to_cell_df(array, list_points, shape, column, lat_point, lon_point, index, spatial_moments = True):

    """
    Get data from 3d or 4d array
    for one cell along time dimension
    Grid contains the lat lon points 
    lat lon are dims -2 and -1
    time is dim 0
    """

    from my_series.convert import cell_to_df


    coords_point                = (lat_point, lon_point)

    indices_cell, coords_cell   = closest_cell(coords_point, list_points, shape)

    y_cell, x_cell              = [*indices_cell]

    array_cell                  = cell(array, y_cell, x_cell)

    timeseries_cell             = cell_to_df(array_cell, column, index = index) 

    return indices_cell, coords_cell, timeseries_cell


def cell(array, y: int, x: int, y_dim: int = -2, x_dim: int = -1):

    """
    Get data from 3d or 4d array
    for one cell along time dimension
    Grid contains the lat lon points 
    lat lon are dims -2 and -1
    time is dim 0
    """
    
    #ndim                        = array.ndim
    #print(ndim)
    #
    #indx                        = [slice(None)] * ndim
    #indx[y_dim]                 = slice(y)
    #indx[x_dim]                 = slice(x)

    cell                        = array[..., y, x]
    
    return cell
        

def cells(array, ys, xs, y_dim: int = -2, x_dim: int = -1):

    cells                       = [cell(array, ys[i], xs[i]) for i in range(len(ys))]

    return cells





