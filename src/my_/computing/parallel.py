
from mpi4py import MPI
from typing import Callable, Any
import numpy as np

from my_.files.netcdf import open, variables_to_array
from my_.files.handy import check_file_exists

def pixel_wise(func: Callable,
               variables: list[str],
               variables_out: list[str],
               files: str,
               file_out: str = 'out.nc',
               dtype: str = 'float32',
               dtype_out: str = 'float32',
               return_shape: int | list[int] | None = None,
               return_dims: str | list[str] = 'time',
               *args, **kwargs) -> Any:
    
    if check_file_exists(file_out): return

    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()
    
    print(f'Rank {rank} out of {size} active.')

    comm.Barrier()

    if rank == 0:

        print(f'Rank {rank} is loading the data...')
        
        data = open(f'{files}')

        arrays = variables_to_array(data, variables, dtype = dtype)

        shape = arrays[0].shape

        if isinstance(return_shape, int): return_shape = [return_shape]

        array_out = np.empty((*return_shape, *shape[-2:]), dtype = dtype_out)
        array_out[:] = np.nan

    elif rank != 0:

        print(f'Rank {rank} creating empty objects...')

        shape = None

    shape = comm.bcast(shape, root = 0)

    if rank != 0:

        print(f'I am rank {rank} and I know the shapes: {shape}. Creating empty arrays...')

        arrays_recv = [np.empty(shape[:-2], dtype = dtype)] * len(variables)


    comm.Barrier()


    print(f'I am rank {rank}. Ready for sending / receiving and calculations.')

    range_y = np.arange(shape[-2])
    range_x = np.arange(shape[-1])
    grid = np.array(np.meshgrid(range_y, range_x))
    cells = grid.T.reshape(-1, 2)
    length = len(cells)
    perrank = length // (size - 1)
    resid = length - perrank * (size - 1)

    for yx in range(perrank):
    
        if rank == 0:

            for r in range(1, size):

                r_n = (size - 1) * yx + (r - 1)
                y = cells[r_n][0]
                x = cells[r_n][1]

                arrays_yx = [array[..., y, x] for array in arrays]

                print(f'Rank {rank} sending cell {r_n} corresponding to')
                print(f'grid indices {x}, {y} to rank {r}.')

                for array in arrays_yx: comm.Send(np.ascontiguousarray(array), dest = r, tag = yx)

                print(f'Rank {rank} succesfully sent data to rank {r}.')
            
            for r in range(1, size):

                r_n = (size - 1) * yx + (r - 1)
                y = cells[r_n][0]
                x = cells[r_n][1]

                print(f'Rank {rank} receiving func {func.__name__} output')
                print(f'from grid indices {x}, {y} to rank {r}.')

                return_object = comm.recv(source = r, tag = yx)

                print(f'Rank {rank} received function output from rank {r},')
                print(f'from grid indices {x}, {y} to rank {r}.')

                array_out[..., y, x] = return_object

        
        if rank != 0:

            r_m = (size - 1) * yx + (rank - 1)
            y = cells[r_m][0]
            x = cells[r_m][1]

            print(f'Rank {rank} receiving cell {r_m} corresponding to')
            print(f'grid indices {x}, {y} from rank 0.')

            for array in arrays_recv: comm.Recv(array, source = 0, tag = yx)

            print(f'Rank {rank} received cell {r_m}.')
            print(f'No executing function {func.__name__}...')

            out_func = func(arrays_recv, *args, **kwargs)

            print(f'Rank {rank} executed function for grid indices {x}, {y}.')
            print(f'Sending back the output to rank 0...')

            comm.send(out_func, dest = 0, tag = yx)
            
            print(f'Rank {rank} succesfully sent function output')
            print(f'for grid indices {x}, {y} to rank 0.')


    comm.Barrier()


    if rank <= resid:

        print(f'Rank {rank} starting residual loop.')

        if rank == 0:
        
            for r in range(1, resid + 1):

                y = cells[-r][0]
                x = cells[-r][1]

                arrays_yx = [array[..., y, x] for array in arrays]

                print(f'Rank {rank} sending cell {-r} corresponding to')
                print(f'grid indices {x}, {y} to rank {r}.')

                for array in arrays_yx: comm.Send(np.ascontiguousarray(array), dest = r, tag = yx)

                print(f'Rank {rank} succesfully sent data to rank {r}.')

            for r in range(1, resid + 1):

                y = cells[-r][0]
                x = cells[-r][1]

                print(f'Rank {rank} receiving func {func.__name__} output')
                print(f'from grid indices {x}, {y} to rank {r}.')

                return_object = comm.recv(source = r, tag = yx)

                print(f'Rank {rank} received function output from rank {r},')
                print(f'from grid indices {x}, {y} to rank {r}.')

                array_out[..., y, x] = return_object


        if rank != 0:

            y = cells[-rank][0]
            x = cells[-rank][1]

            print(f'Rank {rank} receiving cell {-rank} corresponding to')
            print(f'grid indices {x}, {y} from rank 0.')

            for array in arrays_recv: comm.Recv(array, source = 0, tag = yx)

            print(f'Rank {rank} received cell {-rank}.')
            print(f'No executing function {func.__name__}...')

            out_func = func(arrays_recv, *args, **kwargs)

            print(f'Rank {rank} executed function for grid indices {x}, {y}.')
            print(f'Sending back the output to rank 0...')

            comm.send(out_func, dest = 0, tag = yx)
            
            print(f'Rank {rank} succesfully sent function output')
            print(f'for grid indices {x}, {y} to rank 0.')


    comm.Barrier()


    if rank == 0:

        import xarray as xr

        if isinstance(return_dims, str): return_dims = [return_dims]

        out_vars = {v: ([*return_dims, 'lat', 'lon'], array_out) for v in variables_out}

        DS_out = xr.Dataset(data_vars = out_vars)

        print('Now wrinting DS to netcdf...')

        DS_out.to_netcdf(path = file_out, mode='w')

        print('Script was successful! Bye bye!')


if __name__ == '__main__':

    from my_.science.anomalies import standard_index

    pixel_wise(func = standard_index, 
                    variables = ['QFLX_EVAP_GRND'],
                    variables_out = ['SXI_ET_GRND'],
                    files =  '/p/scratch/cjibg31/jibg3105/data/CLM5EU3/006/join_8d/*.nc',
                    file_out = 'SXI_ET_GRND.nc',
                    return_shape = 46*24,
                    return_dims = 'time',
                    year_start = 1995,
                    year_end = 2018)