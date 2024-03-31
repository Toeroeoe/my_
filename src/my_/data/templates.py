from dataclasses import dataclass
import importlib
import os
import numpy as np
import pandas as pd
import pint


@dataclass
class gridded_data:
    
    name: str
    version: tuple[int]
    path: os.PathLike
    type_file: str
    year_start: int
    month_start: int
    year_end: int
    month_end: int
    resolution_time: str
    grid: str
    variables: list[str]
    variable_names: dict
    variable_dimensions: dict
    variable_units: dict
    

    def index_time(self,
                   y0: int | None,
                   y1: int | None):
        
        from my_.series.time import index
        
        if y0 is None: y0 = self.year_start
        elif y0 < self.year_start: y0 = self.year_start
        
        if y1 is None: y1 = self.year_end
        elif y1 > self.year_end: y1 = self.year_end
    
        return index(y0, 
                     y1, 
                     self.resolution_time)
    

    def present_variables(self, 
                          load_variables: list[str]):
        
        variables_present = [v for v in load_variables if v in self.variables]

        return variables_present
    

    def present_source_variables(self,
                                 load_variables: list[str]):
    
        variables_present = self.present_variables(load_variables)
            
        source_variables = [self.variable_names[v] for v in variables_present]
        
        return source_variables
        
    
    def get_values(self,
                   load_variables: list[str],
                   y0: int | None,
                   y1: int | None):
        
        if y0 is None: y0 = self.year_start
        elif y0 < self.year_start: y0 = self.year_start
        
        if y1 is None: y1 = self.year_end
        elif y1 > self.year_end: y1 = self.year_end

        print(f'\nLoading value data for:')
        print(f'{load_variables} from year {y0} to year {y1}...\n')

        type_module = check_module(f'my_.files.{self.type_file}')

        if not type_module: return

        files = [f'{self.path}/{y}.{type_module.file_ending}'
                for y in range(y0, y1 + 1)]

        data = type_module.open(files)

        present_vars = self.present_variables(load_variables)

        present_src_vars = self.present_source_variables(load_variables)
        
        values = type_module.variables_to_array(data, present_src_vars)

        return {v: values[i] for i, v in enumerate(present_vars)}
    

    def get_variables(self, 
                      load_variables: list[str],
                      y0: int | None,
                      y1: int | None):
        
        present_vars = self.present_variables(load_variables)

        values = self.get_values(load_variables,
                                 y0,
                                 y1)
        
        variables = {v: gridded_variables(unit = self.variable_units[v], 
                                         array = values[i] ) 
                                         for i, v in enumerate(present_vars)}
                        
        return variables


    def convert_units(self,
                      values: dict,
                      dst_units: dict):
        
        ureg = pint.UnitRegistry()
        Q_ = ureg.Quantity

        values_out = {}

        for v, array in values.items():

            src_unit = self.variable_units[v]
            dst_unit = dst_units[v]
        
            print(f'\nConverting {v} units from {src_unit} to {dst_unit}...\n')

            values_src = Q_(array, src_unit)

            values_dst = values_src.to(dst_unit)  
            
            values_out[v] = values_dst
    
            print(array.shape, values_dst.shape)

        return values_out


    def regrid():
        ...

    def resample():
        ...


@dataclass
class grid:

    version: tuple[str]
    path_file: os.PathLike
    name_file: str
    type_file: str
    name_latitude: str
    name_longitude: str

    def load_coordinates(self):
        
        type_module = check_module(f'my_.files.{self.type_file}')

        if not type_module: return

        file = f'{self.path_file}/{self.name_file}'

        data = type_module.open(file)

        values = type_module.variables_to_array(data, 
                                                [self.name_latitude, 
                                                self.name_longitude])

        return values


    def points(self):

        lat, lon = self.load_coordinates()

        if (lat.ndim == 1) & (lon.ndim == 1):
            
            stacked_coords = np.array(np.meshgrid(lat, lon))
        
            list_points = stacked_coords.T.reshape(-1, 2)

        elif (lat.ndim == 2) & (lon.ndim == 2):

            stacked_coords = np.dstack([lat, lon])
    
            list_points = stacked_coords.reshape(-1, 2)
    
        return list_points


    def shape(self):

        lat, lon = self.load_coordinates()

        if (lat.ndim == 1) & (lon.ndim == 1):
            
            shape = (*lat.shape, *lon.shape)
    
        elif (lat.ndim == 2) & (lon.ndim == 2):

            shape = lat.shape

        return shape



@dataclass
class gridded_variables:

    unit: str
    array: np.ndarray

    def transform(self, 
                  unit: str):

        ...

def check_module(module: str):

    try:
    
        mod = importlib.import_module(module)
            
        print(f'\nModule {module} imported successfully.\n')

        return mod
    
    except ModuleNotFoundError: 
        
        print(f'\nModule {module} is not yet supported. Continue...\n')
        
        return False


def check_module_var(module: str, 
                     var: str):

    try:
    
        mod = importlib.import_module(module)
            
        print(f'\nModule {module} imported successfully.\n')

        return mod.var
    
    except ModuleNotFoundError: 
        
        print(f'\nModule {module} is not yet supported. Continue...\n')
        
        return False