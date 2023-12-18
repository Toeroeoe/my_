

def open_netcdf(str_files):

    from glob import glob
    from netCDF4 import Dataset, MFDataset
    
    if isinstance(str_files, str):

        files                   = glob(str_files)

        n_files                 = len(files)

        if n_files == 1: return Dataset(files[0])

        data                    = MFDataset(files)

    elif isinstance(str_files, list):

        data                    = MFDataset(str_files)
        
    return data


def netcdf_variable_to_array(Dataset, variable: str, dtype: str = 'float64'):

    import numpy as np

    netcdf_variable         = Dataset.variables[variable]

    array                   = netcdf_variable[:]

    np_dtype                = getattr(np, dtype)
    
    array_dtype             = array.astype(np_dtype)

    return array_dtype
    

def netcdf_variables_to_array(Dataset, variables, dtype: str = 'float64'):
    
    arrays_dtype            = [netcdf_variable_to_array(Dataset, v, dtype) for v in variables]

    return arrays_dtype

