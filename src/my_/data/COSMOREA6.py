from dataclasses import dataclass
from my_.data.templates import gridded_data

@dataclass
class ouput_data(gridded_data):
    pass

all_EUCORDEX_daily = {
    'name': 'BGC_EU3',
    'version': (1, 0, 6),
    'path': '/p/scratch/cjibg31/jibg3105/data/CLM5EU3/006/join_8d/',
    'type_file': 'netcdf',
    'year_start': 1995,
    'month_start': 1,
    'year_end': 2018,
    'month_end': 12,
    'resolution_time': 'D',
    'grid': 'ERA5L_EUCORDEX',
    'variables': ['P', 
                  'ET',
                  'PET'
                  'Runoff',
                  'SM'],
    'variable_names': {'GPP': 'GPP', 
                       'ET': 'QFLX_EVAP_TOT',
                       'Runoff': 'QOVER',
                       'Albedo': 'ALBD',
                       'SM': 'H2OSOI',
                       },
    'variable_dimensions': {'GPP': ['time', 'lat', 'lon'], 
                            'ET': ['time', 'lat', 'lon'],
                            'Runoff': ['time', 'lat', 'lon'],
                            'Albedo': ['time', 'rad', 'lat', 'lon'], # solar radiation bands: vis, nir
                            'SM': ['time', 'layer', 'lat', 'lon']}, 
    'variable_units': {'GPP': 'g/s',
                       'ET': 'mm/s',
                       'Runoff': 'mm/s',
                       'Albedo': '-',
                       'SM': 'mm^3/mm^3'}
}
