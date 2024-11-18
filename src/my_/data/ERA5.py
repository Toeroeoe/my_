import numpy as np
import os
from my_.files.handy import create_dirs, check_file_exists
from glob import glob
import xarray as xr

spinup_forcing_EU3_3h = {
    'name': 'ERA5_forcing_EU3_3h',
    'version': (1, 0, 6),
    'path': '/p/data1/jibg31/FORCINGS/ERA5/',
    'type_file': 'netcdf',
    'year_start': 1950,
    'month_start': 1,
    'year_end': 1959,
    'month_end': 12,
    'resolution_time': '3H',
    'grid': 'EU3',
    'variables': ['P',
                  'Temp',
                  'PSRF',
                  'FSDS',
                  'FLDS',
                  'WIND', 
                  'QBOT',],
    'variable_names': {'P': 'PRECTmms',
                       'Temp': 'TBOT',
                       'PSRF': 'PSRF',
                       'FSDS': 'FSDS',
                       'FLDS': 'FLDS',
                       'WIND': 'WIND',
                       'QBOT': 'QBOT',},
    'variable_dimensions': {'P': ['time', 'lat', 'lon'], 
                            'Temp': ['time', 'lat', 'lon'],
                            'PSRF': ['time', 'lat', 'lon'],
                            'FSDS': ['time', 'lat', 'lon'],
                            'FLDS': ['time', 'lat', 'lon'],
                            'WIND': ['time', 'lat', 'lon'],
                            'QBOT': ['time', 'lat', 'lon'],},
    'variable_units': {'P': 'mm/s',
                       'Temp': 'K',
                       'PSRF': 'Pa',
                       'FSDS': 'W/m^2',
                       'FLDS': 'W/m^2',
                       'WIND': 'm/s',
                       'QBOT': 'kg/kg'},
    'mask_value': None,
    'leapday': False
}



def create_yearly_files(path_rawdata: os.PathLike,
                        path_out: os.PathLike):
    
    create_dirs(path_out)

    files = sorted(glob(f'{path_rawdata}/*.nc'))
    
    data_raw = xr.open_mfdataset(files)

    years = np.unique(data_raw.time.dt.year.values)

    for y in years:

        print(f'Create yearly file for year {y}...\n')

        if check_file_exists(f'{path_out}/{y}.nc'): continue

        data_y = data_raw.sel(time = data_raw.time.dt.year.isin([y]))

        data_y.to_netcdf(f'{path_out}/{y}.nc',
                         format = 'NETCDF4_CLASSIC', 
                         unlimited_dims = ['time'])