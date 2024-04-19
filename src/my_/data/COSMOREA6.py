from dataclasses import dataclass
from my_.data.templates import gridded_data

@dataclass
class ouput_data(gridded_data):
    pass

EUCORDEX_3km_8daily = {
    'name': 'COSMOREA5_EUCORDEX_3km_8daily',
    'version': (1, 0, 0),
    'path': '/p/scratch/cjibg31/jibg3105/data/COSMOREA6/8daily/',
    'type_file': 'netcdf',
    'year_start': 1995,
    'month_start': 1,
    'year_end': 2018,
    'month_end': 12,
    'resolution_time': '8D',
    'grid': 'EU3',
    'variables': [
                  'P',
                  'Temp',
                  'PRSF',
                  'FSDS',
                  'FLDS',
                  'WIND', 
                  'RH',
                 ],
    'variable_names': {
                       'P': 'PRECTmms',
                       'Temp': 'TBOT',
                       'PRSF': 'PRSF',
                       'FSDS': 'FSDS',
                       'FLDS': 'FLDS',
                       'WIND': 'WIND',
                       'RH': 'RH',
                       },
    'variable_dimensions': {
                            'P': ['time', 'lat', 'lon'], 
                            'Temp': ['time', 'lat', 'lon'], 
                            'PRSF': ['time', 'lat', 'lon'], 
                            'FSDS': ['time', 'lat', 'lon'], 
                            'FLDS': ['time', 'lat', 'lon'], 
                            'WIND': ['time', 'lat', 'lon'], 
                            'RH': ['time', 'lat', 'lon'], 
                           }, 
    'variable_units': {
                       'P': 'mm/s',
                       'Temp': 'K',
                       'PRSF': 'Pa',
                       'FSDS': 'W/m^2',
                       'FLDS': 'W/m^2',
                       'WIND': 'm/s',
                       'RH': '%',
                      },
    'mask_value': None
}


EUCORDEX_3km_daily = {
    'name': 'COSMOREA5_EUCORDEX_3km_daily',
    'version': (1, 0, 0),
    'path': '/p/scratch/cjibg31/jibg3105/CESMDataRoot/InputData/Forcings/COSMOREA6/yearly_files/',
    'type_file': 'netcdf',
    'year_start': 1995,
    'month_start': 1,
    'year_end': 2018,
    'month_end': 12,
    'resolution_time': 'D',
    'grid': 'EU3',
    'variables': [
                  'P',
                  'Temp',
                  'PSRF',
                  'FSDS',
                  'FLDS',
                  'WIND', 
                  'RH',
                 ],
    'variable_names': {
                       'P': 'PRECTmms',
                       'Temp': 'TBOT',
                       'PSRF': 'PSRF',
                       'FSDS': 'FSDS',
                       'FLDS': 'FLDS',
                       'WIND': 'WIND',
                       'RH': 'RH',
                       },
    'variable_dimensions': {
                            'P': ['time', 'lat', 'lon'], 
                            'Temp': ['time', 'lat', 'lon'], 
                            'PSRF': ['time', 'lat', 'lon'], 
                            'FSDS': ['time', 'lat', 'lon'], 
                            'FLDS': ['time', 'lat', 'lon'], 
                            'WIND': ['time', 'lat', 'lon'], 
                            'RH': ['time', 'lat', 'lon'], 
                           }, 
    'variable_units': {
                       'P': 'mm/s',
                       'Temp': 'K',
                       'PSRF': 'Pa',
                       'FSDS': 'W/m^2',
                       'FLDS': 'W/m^2',
                       'WIND': 'm/s',
                       'RH': '%',
                      },
    'mask_value': None
}