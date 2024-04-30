from dataclasses import dataclass
import importlib
import os
import numpy as np
import pandas as pd
import pint
import xarray as xr
import pint_xarray
from glob import glob

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
    mask_value: None | float | int
    

    def index_time(self,
                   y0: int | None = None,
                   y1: int | None = None):
        
        from my_.series.time import index
        
        if y0 is None: y0 = self.year_start
        elif y0 < self.year_start: y0 = self.year_start
        
        if y1 is None: y1 = self.year_end
        elif y1 > self.year_end: y1 = self.year_end
    
        return index(y0, 
                     y1, 
                     self.resolution_time)
    
    def present_files(self,
                      y0: int | None,
                      y1: int | None):
        
        if y0 is None: y0 = self.year_start
        elif y0 < self.year_start: y0 = self.year_start
        
        if y1 is None: y1 = self.year_end
        elif y1 > self.year_end: y1 = self.year_end
    
        files = [f'{self.path}/{y}.nc' for y in np.arange(y0, y1 +1)]

        return files

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

        type_module = check_data_module('my_.files',
                                        self.type_file)

        if not type_module: return

        files = [f'{self.path}/{y}.{type_module.file_ending}'
                for y in range(y0, y1 + 1)]

        data = type_module.open(files)

        present_vars = self.present_variables(load_variables)

        present_src_vars = self.present_source_variables(load_variables)
        
        values = type_module.variables_to_array(data, 
                                                present_src_vars,
                                                mask_value = self.mask_value)

        return {v: values[i] for i, v in enumerate(present_vars)}
    

    def get_variables(self, 
                      load_variables: list[str],
                      y0: int | None,
                      y1: int | None):
        
        if y0 is None: y0 = self.year_start
        elif y0 < self.year_start: y0 = self.year_start
        
        if y1 is None: y1 = self.year_end
        elif y1 > self.year_end: y1 = self.year_end

        print(f'\nLoading data for:')
        print(f'{load_variables} from year {y0} to year {y1}...\n')
        
        present_vars = self.present_variables(load_variables)

        type_module = check_data_module('my_.files',
                                        self.type_file)

        files = [f'{self.path}/{y}.{type_module.file_ending}'
                for y in range(y0, y1 + 1)]
        
        data = xr.open_mfdataset(files) if len(files) > 1 else xr.open_dataset(files[0])

        name_dict = {v: k for k, v in self.variable_names.items() if k in present_vars} 
    
        data_s = data.rename(name_dict)
                      
        data_v = data_s[present_vars]
                        
        return data_v


    def convert_units(self,
                      values: dict | xr.Dataset | xr.DataArray,
                      dst_units: dict,
                      variables: None | dict = None):
        
        ureg = pint.UnitRegistry()
        Q_ = ureg.Quantity

        values_out = {} if isinstance(values, dict) else values.copy()

        for i, (v, array) in enumerate(values.items()):

            vi = variables[v] if variables is not None else v

            src_unit = self.variable_units[vi]
            dst_unit = dst_units[vi]
        
            print(f'\nConverting {vi} units from {src_unit} to {dst_unit}...\n')

            if isinstance(array, np.ndarray):
                
                Q_ = ureg.Quantity
                
                values = Q_(array, src_unit)
                
                values_dst = values.to(dst_unit)

                values_out[v] = values_dst.magnitude

            elif isinstance(array, xr.DataArray):
    
                values = array.pint.quantify(src_unit)

                values_dst = values.pint.to(dst_unit)

                values_out[v] = values_dst.pint.dequantify()

        return values_out


    def regrid():
        ...

    def resample(self,
                 dataset: xr.DataArray | xr.Dataset,
                 dst_time_res: str,
                 method: str | list,
                 var_subset: list | None = None,
                 **kwargs) -> xr.Dataset | xr.DataArray:

        from my_.series.interpolate import resample
        
        if var_subset is not None: dataset = dataset[var_subset]

        if isinstance(method, list):

            out_ds = xr.Dataset()
            
            for m in method:

                ds = resample(dataset, dst_time_res, m, **kwargs)
    
                new_names = {n: f'{n}_{m}' for n in ds.keys()}
    
                ds_new = ds.rename(new_names)
        
                out_ds.update(ds_new)

        elif isinstance(method, str):

            out_ds = resample(dataset, dst_time_res, method, **kwargs)
    
        return out_ds


@dataclass
class grid:

    name: str
    version: tuple[str]
    path_file: os.PathLike
    name_file: str
    type_file: str
    name_latitude: str
    name_longitude: str

    def load_coordinates(self):
        
        type_module = check_data_module('my_.files',
                                        self.type_file)
        
        print(f'\nLoad lat and lon variables from grid {self.name}...\n')

        if not type_module: return

        file = f'{self.path_file}/{self.name_file}'

        print(file)

        data = type_module.open(file)

        values = type_module.variables_to_array(data, 
                                                [self.name_latitude, 
                                                self.name_longitude])

        return values


    def points(self):

        lat, lon = self.load_coordinates()

        if (lat.ndim == 1) & (lon.ndim == 1):
            
            stacked_coords = np.array(np.meshgrid(lat, 
                                                  lon))
        
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

def check_data_module(package_str: str, 
                      module_str: str):

    module_ = module_str.split('_')[0]
    attribute_ = '_'.join(module_str.split('_')[1:])

    try:
    
        mod = importlib.import_module(f'{package_str}.{module_}')
            
        print(f'\nModule {module_} imported successfully.\n')
        
        if attribute_ == '': return mod

        out = getattr(mod, attribute_)

        return out
    
    except ModuleNotFoundError: 
        
        print(f'\nModule {module_str} is not yet supported. Continue...\n')
        
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