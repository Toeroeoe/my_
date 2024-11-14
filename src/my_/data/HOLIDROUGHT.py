from dataclasses import dataclass
import pandas as pd
from glob import glob
import xarray as xr
import numpy as np
import os 

from my_.files.handy import create_dirs, check_file_exists
from my_.data.templates import gridded_data

@dataclass
class cluster_data(gridded_data):
    
    agg_period: str
    filter_area: float # [km²]
    weigh_mid: float
    weigh_steep: float
    grid_window: int
    frac_points: float
    factor_time: float
    km_per_cell: float = 9


    def __post_init__(self):
        
        self.path = self.path + \
                    f'/{self.agg_period}_' + \
                    f'l-{self.grid_window}_' + \
                    f'p-{self.frac_points}_' + \
                    f'k-{self.weigh_mid}_' + \
                    f'e-{self.weigh_steep}_' + \
                    f'a-{self.filter_area}_' + \
                    f't-{self.factor_time}_' + \
                    f'y0-{self.year_start}_' + \
                    f'y1-{self.year_end}/'

    def get_file_fix(self):
        
        str_f = f'{self.agg_period}_' + \
                f'l-{self.grid_window}_' + \
                f'p-{self.frac_points}_' + \
                f'k-{self.weigh_mid}_' + \
                f'e-{self.weigh_steep}_' + \
                f'a-{self.filter_area}_' + \
                f't-{self.factor_time}_' + \
                f'y0-{self.year_start}_' + \
                f'y1-{self.year_end}'
        
        return str_f
    
    def get_properties(self, variable):

        dir_file = '/p/scratch/cjibg31/jibg3105/projects/papers/CLM5EU3_Droughts/out/cluster_properties'

        name_file = self.get_file_fix()

        properties = pd.read_excel(f'{dir_file}/{variable}_{name_file}.xlsx', 
                           header = [0, 1],
                           index_col = 0)
        
        return properties
    
variables_EU3_8daily = {
    'name': 'HOLIDROUGHT_BGC_EU3_variables',
    'version': (0, 1, 0),
    'path': '/p/scratch/cjibg31/jibg3105/data/HOLIDROUGHT/variables/',
    'type_file': 'netcdf',
    'year_start': 1995,
    'month_start': 1,
    'year_end': 2018,
    'month_end': 12,
    'leapday': False,
    'resolution_time': '8D',
    'grid': 'EU3',
    'variables': ['GPP', 
                  'ESOIL',
                  'Tr',
                  'BTRAN',
                  'Gs',
                  'Runoff',
                  'SM',
                  'WTD',
                  'VPD',
                  'P'],
    'variable_names': {'GPP': 'GPP', 
                       'ESOIL': 'ESOIL',
                       'Tr': 'Tr',
                       'BTRAN': 'BTRAN',
                       'Gs': 'Gs',
                       'Runoff': 'Runoff',
                       'SM': 'SM',
                       'WTD': 'WTD',
                       'VPD': 'VPD',
                       'P': 'P'},
    'variable_dimensions': {'GPP': ['time', 'lat', 'lon'], 
                            'ESOIL': ['time', 'lat', 'lon'],
                            'Tr': ['time', 'lat', 'lon'],  
                            'BTRAN': ['time', 'lat', 'lon'],
                            'Gs': ['time', 'lat', 'lon'],
                            'Runoff': ['time', 'lat', 'lon'],
                            'SM': ['time', 'layer', 'lat', 'lon'],
                            'WTD': ['time', 'lat', 'lon'],
                            'VPD': ['time', 'lat', 'lon'],
                            'P': ['time', 'lat', 'lon']}, 
    'variable_units': {'GPP': 'g/day',
                       'ESOIL': 'mm/day',
                       'Tr': 'mm/day',
                       'BTRAN': 'dimensionless',
                       'Gs': 'umol/day',
                       'Runoff': 'mm/day',
                       'SM': 'm^3/m^3',
                       'WTD': 'm',
                       'VPD': 'kPa',
                       'P': 'mm/day'},
    'mask_value': None
}


SXI_365D_EU3_8daily = {
    'name': 'HOLIDROUGHT_SXI_365D',
    'version': (0, 1, 0),
    'path': '/p/scratch/cjibg31/jibg3105/data/HOLIDROUGHT/SXI/365D/',
    'type_file': 'netcdf',
    'year_start': 1996,
    'month_start': 1,
    'year_end': 2018,
    'month_end': 12,
    'resolution_time': '8D',
    'grid': 'EU3',
    'leapday': False,
    'variables': ['SXI_GPP', 
                  'SXI_ESOIL',
                  'SXI_Tr',
                  'SXI_BTRAN',
                  'SXI_Gs',
                  'SXI_Runoff',
                  'SXI_SM',
                  'SXI_WTD',
                  'SXI_VPD',
                  'SXI_P'],
    'variable_names': {'SXI_GPP': 'SXI_GPP', 
                       'SXI_ESOIL': 'SXI_ESOIL',
                       'SXI_Tr': 'SXI_Tr',
                       'SXI_BTRAN': 'SXI_BTRAN',
                       'SXI_Gs': 'SXI_Gs',
                       'SXI_Runoff': 'SXI_Runoff',
                       'SXI_SM': 'SXI_SM_0',
                       'SXI_WTD': 'SXI_WTD',
                       'SXI_VPD': 'SXI_VPD',
                       'SXI_P': 'SXI_P'},
    'variable_dimensions': {'SXI_GPP': ['time', 'lat', 'lon'], 
                            'SXI_ESOIL': ['time', 'lat', 'lon'],
                            'SXI_Tr': ['time', 'lat', 'lon'],  
                            'SXI_BTRAN': ['time', 'lat', 'lon'],
                            'SXI_Gs': ['time', 'lat', 'lon'],
                            'SXI_Runoff': ['time', 'lat', 'lon'],
                            'SXI_SM': ['time', 'layer', 'lat', 'lon'],
                            'SXI_WTD': ['time', 'lat', 'lon'],
                            'SXI_VPD': ['time', 'lat', 'lon'],
                            'SXI_P': ['time', 'lat', 'lon']}, 
    'variable_units': {'SXI_GPP': 'dimensionless',
                       'SXI_ESOIL': 'dimensionless',
                       'SXI_Tr': 'dimensionless',
                       'SXI_BTRAN': 'dimensionless',
                       'SXI_Gs': 'dimensionless',
                       'SXI_Runoff': 'dimensionless',
                       'SXI_SM': 'dimensionless',
                       'SXI_WTD': 'dimensionless',
                       'SXI_VPD': 'dimensionless',
                       'SXI_P': 'dimensionless'},
    'mask_value': None
}


SXI_183D_EU3_8daily = {
    'name': 'HOLIDROUGHT_SXI_183D',
    'version': (0, 1, 0),
    'path': '/p/scratch/cjibg31/jibg3105/data/HOLIDROUGHT/SXI/183D/',
    'type_file': 'netcdf',
    'year_start': 1995,
    'month_start': 6,
    'year_end': 2018,
    'month_end': 12,
    'leapday': False,
    'resolution_time': '8D',
    'grid': 'EU3',
    'variables': ['SXI_GPP', 
                  'SXI_ESOIL',
                  'SXI_Tr',
                  'SXI_BTRAN',
                  'SXI_Gs',
                  'SXI_Runoff',
                  'SXI_SM',
                  'SXI_WTD',
                  'SXI_VPD',
                  'SXI_P'],
    'variable_names': {'SXI_GPP': 'SXI_GPP', 
                       'SXI_ESOIL': 'SXI_ESOIL',
                       'SXI_Tr': 'SXI_Tr',
                       'SXI_BTRAN': 'SXI_BTRAN',
                       'SXI_Gs': 'SXI_Gs',
                       'SXI_Runoff': 'SXI_Runoff',
                       'SXI_SM': 'SXI_SM_0',
                       'SXI_WTD': 'SXI_WTD',
                       'SXI_VPD': 'SXI_VPD',
                       'SXI_P': 'SXI_P'},
    'variable_dimensions': {'SXI_GPP': ['time', 'lat', 'lon'], 
                            'SXI_ESOIL': ['time', 'lat', 'lon'],
                            'SXI_Tr': ['time', 'lat', 'lon'],  
                            'SXI_BTRAN': ['time', 'lat', 'lon'],
                            'SXI_Gs': ['time', 'lat', 'lon'],
                            'SXI_Runoff': ['time', 'lat', 'lon'],
                            'SXI_SM': ['time', 'layer', 'lat', 'lon'],
                            'SXI_WTD': ['time', 'lat', 'lon'],
                            'SXI_VPD': ['time', 'lat', 'lon'],
                            'SXI_P': ['time', 'lat', 'lon']}, 
    'variable_units': {'SXI_GPP': 'dimensionless',
                       'SXI_ESOIL': 'dimensionless',
                       'SXI_Tr': 'dimensionless',
                       'SXI_BTRAN': 'dimensionless',
                       'SXI_Gs': 'dimensionless',
                       'SXI_Runoff': 'dimensionless',
                       'SXI_SM': 'dimensionless',
                       'SXI_WTD': 'dimensionless',
                       'SXI_VPD': 'dimensionless',
                       'SXI_P': 'dimensionless'},
    'mask_value': None
}

SXI_92D_EU3_8daily = {
    'name': 'HOLIDROUGHT_SXI_92D',
    'version': (0, 1, 0),
    'path': '/p/scratch/cjibg31/jibg3105/data/HOLIDROUGHT/SXI/92D/',
    'type_file': 'netcdf',
    'year_start': 1995,
    'month_start': 4,
    'year_end': 2018,
    'month_end': 12,
    'leapday': False,
    'resolution_time': '8D',
    'grid': 'EU3',
    'variables': ['SXI_GPP', 
                  'SXI_ESOIL',
                  'SXI_Tr',
                  'SXI_BTRAN',
                  'SXI_Gs',
                  'SXI_Runoff',
                  'SXI_SM',
                  'SXI_WTD',
                  'SXI_VPD',
                  'SXI_P'],
    'variable_names': {'SXI_GPP': 'SXI_GPP', 
                       'SXI_ESOIL': 'SXI_ESOIL',
                       'SXI_Tr': 'SXI_Tr',
                       'SXI_BTRAN': 'SXI_BTRAN',
                       'SXI_Gs': 'SXI_Gs',
                       'SXI_Runoff': 'SXI_Runoff',
                       'SXI_SM': 'SXI_SM_0',
                       'SXI_WTD': 'SXI_WTD',
                       'SXI_VPD': 'SXI_VPD',
                       'SXI_P': 'SXI_P'},
    'variable_dimensions': {'SXI_GPP': ['time', 'lat', 'lon'], 
                            'SXI_ESOIL': ['time', 'lat', 'lon'],
                            'SXI_Tr': ['time', 'lat', 'lon'],  
                            'SXI_BTRAN': ['time', 'lat', 'lon'],
                            'SXI_Gs': ['time', 'lat', 'lon'],
                            'SXI_Runoff': ['time', 'lat', 'lon'],
                            'SXI_SM': ['time', 'layer', 'lat', 'lon'],
                            'SXI_WTD': ['time', 'lat', 'lon'],
                            'SXI_VPD': ['time', 'lat', 'lon'],
                            'SXI_P': ['time', 'lat', 'lon']}, 
    'variable_units': {'SXI_GPP': 'dimensionless',
                       'SXI_ESOIL': 'dimensionless',
                       'SXI_Tr': 'dimensionless',
                       'SXI_BTRAN': 'dimensionless',
                       'SXI_Gs': 'dimensionless',
                       'SXI_Runoff': 'dimensionless',
                       'SXI_SM': 'dimensionless',
                       'SXI_WTD': 'dimensionless',
                       'SXI_VPD': 'dimensionless',
                       'SXI_P': 'dimensionless'},
    'mask_value': None
}


SXI_31D_EU3_8daily = {
    'name': 'HOLIDROUGHT_SXI_31D',
    'version': (0, 1, 0),
    'path': '/p/scratch/cjibg31/jibg3105/data/HOLIDROUGHT/SXI/31D/',
    'type_file': 'netcdf',
    'year_start': 1995,
    'month_start': 2,
    'year_end': 2018,
    'month_end': 12,
    'leapday': False,
    'resolution_time': '8D',
    'grid': 'EU3',
    'variables': ['SXI_GPP', 
                  'SXI_ESOIL',
                  'SXI_Tr',
                  'SXI_BTRAN',
                  'SXI_Gs',
                  'SXI_Runoff',
                  'SXI_SM',
                  'SXI_WTD',
                  'SXI_VPD',
                  'SXI_P'],
    'variable_names': {'SXI_GPP': 'SXI_GPP', 
                       'SXI_ESOIL': 'SXI_ESOIL',
                       'SXI_Tr': 'SXI_Tr',
                       'SXI_BTRAN': 'SXI_BTRAN',
                       'SXI_Gs': 'SXI_Gs',
                       'SXI_Runoff': 'SXI_Runoff',
                       'SXI_SM': 'SXI_SM_0',
                       'SXI_WTD': 'SXI_WTD',
                       'SXI_VPD': 'SXI_VPD',
                       'SXI_P': 'SXI_P'},
    'variable_dimensions': {'SXI_GPP': ['time', 'lat', 'lon'], 
                            'SXI_ESOIL': ['time', 'lat', 'lon'],
                            'SXI_Tr': ['time', 'lat', 'lon'],  
                            'SXI_BTRAN': ['time', 'lat', 'lon'],
                            'SXI_Gs': ['time', 'lat', 'lon'],
                            'SXI_Runoff': ['time', 'lat', 'lon'],
                            'SXI_SM': ['time', 'layer', 'lat', 'lon'],
                            'SXI_WTD': ['time', 'lat', 'lon'],
                            'SXI_VPD': ['time', 'lat', 'lon'],
                            'SXI_P': ['time', 'lat', 'lon']}, 
    'variable_units': {'SXI_GPP': 'dimensionless',
                       'SXI_ESOIL': 'dimensionless',
                       'SXI_Tr': 'dimensionless',
                       'SXI_BTRAN': 'dimensionless',
                       'SXI_Gs': 'dimensionless',
                       'SXI_Runoff': 'dimensionless',
                       'SXI_SM': 'dimensionless',
                       'SXI_WTD': 'dimensionless',
                       'SXI_VPD': 'dimensionless',
                       'SXI_P': 'dimensionless'},
    'mask_value': None
}


cluster_365D_EU3_8daily = {
    'name': 'HOLIDROUGHT_clusters_365D',
    'version': (0, 1, 0),
    'path': '/p/scratch/cjibg31/jibg3105/data/HOLIDROUGHT/cluster/',
    'type_file': 'netcdf',
    'year_start': 1996,
    'month_start': 1,
    'year_end': 2018,
    'month_end': 12,
    'resolution_time': '8D',
    'grid': 'EU3',
    'leapday': False,

    'variables': ['SXI_GPP', 
                  'SXI_ESOIL',
                  'SXI_Tr',
                  'SXI_BTRAN',
                  'SXI_Gs',
                  'SXI_Runoff',
                  'SXI_SM',
                  'SXI_WTD',
                  'SXI_VPD',
                  'SXI_P'],
    'variable_names': {'SXI_GPP': 'SXI_GPP', 
                       'SXI_ESOIL': 'SXI_ESOIL',
                       'SXI_Tr': 'SXI_Tr',
                       'SXI_BTRAN': 'SXI_BTRAN',
                       'SXI_Gs': 'SXI_Gs',
                       'SXI_Runoff': 'SXI_Runoff',
                       'SXI_SM': 'SXI_SM',
                       'SXI_WTD': 'SXI_WTD',
                       'SXI_VPD': 'SXI_VPD',
                       'SXI_P': 'SXI_P'},
    'variable_dimensions': {'SXI_GPP': ['time', 'lat', 'lon'], 
                            'SXI_ESOIL': ['time', 'lat', 'lon'],
                            'SXI_Tr': ['time', 'lat', 'lon'],  
                            'SXI_BTRAN': ['time', 'lat', 'lon'],
                            'SXI_Gs': ['time', 'lat', 'lon'],
                            'SXI_Runoff': ['time', 'lat', 'lon'],
                            'SXI_SM': ['time', 'layer', 'lat', 'lon'],
                            'SXI_WTD': ['time', 'lat', 'lon'],
                            'SXI_VPD': ['time', 'lat', 'lon'],
                            'SXI_P': ['time', 'lat', 'lon']}, 
    'variable_units': {'SXI_GPP': 'dimensionless',
                       'SXI_ESOIL': 'dimensionless',
                       'SXI_Tr': 'dimensionless',
                       'SXI_BTRAN': 'dimensionless',
                       'SXI_Gs': 'dimensionless',
                       'SXI_Runoff': 'dimensionless',
                       'SXI_SM': 'dimensionless',
                       'SXI_WTD': 'dimensionless',
                       'SXI_VPD': 'dimensionless',
                       'SXI_P': 'dimensionless'},
    'mask_value': None,

    'agg_period': '365D',
    'grid_window': 3,
    'frac_points': 0.1,
    'weigh_mid': -1.4,
    'weigh_steep': 6.0,
    'filter_area': 30000.0,
    'factor_time': 1.0,
}

cluster_183D_EU3_8daily = {
    'name': 'HOLIDROUGHT_clusters_183D',
    'version': (0, 1, 0),
    'path': '/p/scratch/cjibg31/jibg3105/data/HOLIDROUGHT/cluster/',
    'type_file': 'netcdf',
    'year_start': 1995,
    'month_start': 7,
    'year_end': 2018,
    'month_end': 12,
    'resolution_time': '8D',
    'grid': 'EU3',
    'leapday': False,

    'variables': ['SXI_GPP', 
                  'SXI_ESOIL',
                  'SXI_Tr',
                  'SXI_BTRAN',
                  'SXI_Gs',
                  'SXI_Runoff',
                  'SXI_SM',
                  'SXI_WTD',
                  'SXI_VPD',
                  'SXI_P'],
    'variable_names': {'SXI_GPP': 'SXI_GPP', 
                       'SXI_ESOIL': 'SXI_ESOIL',
                       'SXI_Tr': 'SXI_Tr',
                       'SXI_BTRAN': 'SXI_BTRAN',
                       'SXI_Gs': 'SXI_Gs',
                       'SXI_Runoff': 'SXI_Runoff',
                       'SXI_SM': 'SXI_SM',
                       'SXI_WTD': 'SXI_WTD',
                       'SXI_VPD': 'SXI_VPD',
                       'SXI_P': 'SXI_P'},
    'variable_dimensions': {'SXI_GPP': ['time', 'lat', 'lon'], 
                            'SXI_ESOIL': ['time', 'lat', 'lon'],
                            'SXI_Tr': ['time', 'lat', 'lon'],  
                            'SXI_BTRAN': ['time', 'lat', 'lon'],
                            'SXI_Gs': ['time', 'lat', 'lon'],
                            'SXI_Runoff': ['time', 'lat', 'lon'],
                            'SXI_SM': ['time', 'layer', 'lat', 'lon'],
                            'SXI_WTD': ['time', 'lat', 'lon'],
                            'SXI_VPD': ['time', 'lat', 'lon'],
                            'SXI_P': ['time', 'lat', 'lon']}, 
    'variable_units': {'SXI_GPP': 'dimensionless',
                       'SXI_ESOIL': 'dimensionless',
                       'SXI_Tr': 'dimensionless',
                       'SXI_BTRAN': 'dimensionless',
                       'SXI_Gs': 'dimensionless',
                       'SXI_Runoff': 'dimensionless',
                       'SXI_SM': 'dimensionless',
                       'SXI_WTD': 'dimensionless',
                       'SXI_VPD': 'dimensionless',
                       'SXI_P': 'dimensionless'},
    'mask_value': None,

    'agg_period': '183D',
    'grid_window': 3,
    'frac_points': 0.1,
    'weigh_mid': -1.4,
    'weigh_steep': 6.0,
    'filter_area': 30000.0,
    'factor_time': 1.0,
}

cluster_92D_EU3_8daily = {
    'name': 'HOLIDROUGHT_clusters_92D',
    'version': (0, 1, 0),
    'path': '/p/scratch/cjibg31/jibg3105/data/HOLIDROUGHT/cluster/',
    'type_file': 'netcdf',
    'year_start': 1995,
    'month_start': 4,
    'year_end': 2018,
    'month_end': 12,
    'resolution_time': '8D',
    'grid': 'EU3',
    'leapday': False,

    'variables': ['SXI_GPP', 
                  'SXI_ESOIL',
                  'SXI_Tr',
                  'SXI_BTRAN',
                  'SXI_Gs',
                  'SXI_Runoff',
                  'SXI_SM',
                  'SXI_WTD',
                  'SXI_VPD',
                  'SXI_P'],
    'variable_names': {'SXI_GPP': 'SXI_GPP', 
                       'SXI_ESOIL': 'SXI_ESOIL',
                       'SXI_Tr': 'SXI_Tr',
                       'SXI_BTRAN': 'SXI_BTRAN',
                       'SXI_Gs': 'SXI_Gs',
                       'SXI_Runoff': 'SXI_Runoff',
                       'SXI_SM': 'SXI_SM',
                       'SXI_WTD': 'SXI_WTD',
                       'SXI_VPD': 'SXI_VPD',
                       'SXI_P': 'SXI_P'},
    'variable_dimensions': {'SXI_GPP': ['time', 'lat', 'lon'], 
                            'SXI_ESOIL': ['time', 'lat', 'lon'],
                            'SXI_Tr': ['time', 'lat', 'lon'],  
                            'SXI_BTRAN': ['time', 'lat', 'lon'],
                            'SXI_Gs': ['time', 'lat', 'lon'],
                            'SXI_Runoff': ['time', 'lat', 'lon'],
                            'SXI_SM': ['time', 'layer', 'lat', 'lon'],
                            'SXI_WTD': ['time', 'lat', 'lon'],
                            'SXI_VPD': ['time', 'lat', 'lon'],
                            'SXI_P': ['time', 'lat', 'lon']}, 
    'variable_units': {'SXI_GPP': 'dimensionless',
                       'SXI_ESOIL': 'dimensionless',
                       'SXI_Tr': 'dimensionless',
                       'SXI_BTRAN': 'dimensionless',
                       'SXI_Gs': 'dimensionless',
                       'SXI_Runoff': 'dimensionless',
                       'SXI_SM': 'dimensionless',
                       'SXI_WTD': 'dimensionless',
                       'SXI_VPD': 'dimensionless',
                       'SXI_P': 'dimensionless'},
    'mask_value': None,

    'agg_period': '92D',
    'grid_window': 3,
    'frac_points': 0.1,
    'weigh_mid': -1.4,
    'weigh_steep': 6.0,
    'filter_area': 30000.0,
    'factor_time': 1.0,
}

cluster_31D_EU3_8daily = {
    'name': 'HOLIDROUGHT_clusters_31D',
    'version': (0, 1, 0),
    'path': '/p/scratch/cjibg31/jibg3105/data/HOLIDROUGHT/cluster/',
    'type_file': 'netcdf',
    'year_start': 1995,
    'month_start': 2,
    'year_end': 2018,
    'month_end': 12,
    'resolution_time': '8D',
    'grid': 'EU3',
    'leapday': False,

    'variables': ['SXI_GPP', 
                  'SXI_ESOIL',
                  'SXI_Tr',
                  'SXI_BTRAN',
                  'SXI_Gs',
                  'SXI_Runoff',
                  'SXI_SM',
                  'SXI_WTD',
                  'SXI_VPD',
                  'SXI_P'],
    'variable_names': {'SXI_GPP': 'SXI_GPP', 
                       'SXI_ESOIL': 'SXI_ESOIL',
                       'SXI_Tr': 'SXI_Tr',
                       'SXI_BTRAN': 'SXI_BTRAN',
                       'SXI_Gs': 'SXI_Gs',
                       'SXI_Runoff': 'SXI_Runoff',
                       'SXI_SM': 'SXI_SM',
                       'SXI_WTD': 'SXI_WTD',
                       'SXI_VPD': 'SXI_VPD',
                       'SXI_P': 'SXI_P'},
    'variable_dimensions': {'SXI_GPP': ['time', 'lat', 'lon'], 
                            'SXI_ESOIL': ['time', 'lat', 'lon'],
                            'SXI_Tr': ['time', 'lat', 'lon'],  
                            'SXI_BTRAN': ['time', 'lat', 'lon'],
                            'SXI_Gs': ['time', 'lat', 'lon'],
                            'SXI_Runoff': ['time', 'lat', 'lon'],
                            'SXI_SM': ['time', 'layer', 'lat', 'lon'],
                            'SXI_WTD': ['time', 'lat', 'lon'],
                            'SXI_VPD': ['time', 'lat', 'lon'],
                            'SXI_P': ['time', 'lat', 'lon']}, 
    'variable_units': {'SXI_GPP': 'dimensionless',
                       'SXI_ESOIL': 'dimensionless',
                       'SXI_Tr': 'dimensionless',
                       'SXI_BTRAN': 'dimensionless',
                       'SXI_Gs': 'dimensionless',
                       'SXI_Runoff': 'dimensionless',
                       'SXI_SM': 'dimensionless',
                       'SXI_WTD': 'dimensionless',
                       'SXI_VPD': 'dimensionless',
                       'SXI_P': 'dimensionless'},
    'mask_value': None,

    'agg_period': '31D',
    'grid_window': 3,
    'frac_points': 0.1,
    'weigh_mid': -1.4,
    'weigh_steep': 6.0,
    'filter_area': 30000.0,
    'factor_time': 1.0,
}

def create_yearly_files(path_rawdata: os.PathLike,
                        file: str,
                        path_out: os.PathLike,
                        time_index: pd.Series | pd.Index):
    
    """
    Input directory should only contain the GLEAM rawdata files...
    """
    
    create_dirs(path_out)

    files = glob(f'{path_rawdata}/{file}')

    data_raw = xr.open_mfdataset(files)
    
    data_raw = data_raw.assign_coords(time = time_index)

    years = np.unique(data_raw.time.dt.year.values)

    for y in years:

        print(f'Create yearly file for year {y}...\n')

        if check_file_exists(f'{path_out}/{y}.nc'): continue

        data_y = data_raw.sel(time = data_raw.time.dt.year.isin([y]))

        data_y.to_netcdf(f'{path_out}/{y}.nc',
                         format = 'NETCDF4_CLASSIC', 
                         unlimited_dims = ['time'])