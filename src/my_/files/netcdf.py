
from netCDF4 import Dataset, MFDataset

file_ending = 'nc'

def open(str_files: str):

    from glob import glob
    
    if isinstance(str_files, str):

        files                   = glob(str_files)

        n_files                 = len(files)

        if n_files == 1: return Dataset(files[0])

        data                    = MFDataset(files)

    elif isinstance(str_files, list):

        data                    = MFDataset(str_files)
        
    return data


def variable_to_array(data: Dataset, 
                      variable: str, 
                      stack_axis: int = 1,
                      dtype: str = 'float64'):

    import numpy as np

    if isinstance(variable, list):

        arrays = [data.variables[v][:] 
                  for v in variable]

        array = np.stack(arrays, 
                         axis = stack_axis)

    elif isinstance(variable, str):

        netcdf_variable = data.variables[variable]

        array = netcdf_variable[:]

    np_dtype = getattr(np, dtype)
    
    array_dtype = array.astype(np_dtype)

    return array_dtype
    

def variables_to_array(data: Dataset, 
                       variables: list[str],
                       stack_axis: int = 1, 
                       dtype: str = 'float64'):
    
    arrays_dtype            = [variable_to_array(data, 
                                                 v, 
                                                 stack_axis,
                                                 dtype) for v in variables]

    return arrays_dtype

