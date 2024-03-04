
from mpi4py import MPI
from typing import Callable, Any

from my_files.netcdf import open_netcdf, netcdf_variables_to_array

import numpy as np


def pixel_wise_w0(func: Callable,
                    variables: list[str],
                    files: str,
                    axis: int = 0,
                    dtype: str = 'float32',
                    return_object: Any | None = None,
                    *args, **kwargs) -> Any:

    # works with 3d array, func along axis 0
    # maybe, later, we can implement an "axis" feature
    # Now only compatible when all the variables that
    # func takes are in one netcdf Dataset (or MFDataset)
    
    comm                        = MPI.COMM_WORLD
    rank                        = comm.Get_rank()
    size                        = comm.Get_size()
    
    print(f'Rank {rank} out of {size} active.')

    comm.Barrier()

    if rank == 0:

        print(f'Rank {rank} is loading the data...')
        
        data                    = open_netcdf(f'{files}')

        arrays                  = netcdf_variables_to_array(data, variables, dtype = dtype)

        shape                   = arrays[0].shape

    elif rank != 0:

        print(f'Rank {rank} creating empty objects...')

        shape                   = None

    shape                       = comm.bcast(shape, root = 0)

    if rank != 0:

        print(f'I am rank {rank} and I know the shapes: {shape}. Creating empty arrays...')

        arrays_recv             = [np.empty(shape[:-2], dtype = dtype)] * len(variables)

    comm.Barrier()

    print(f'I am rank {rank}. Ready for sending / receiving and calculations.')

    range_y                     = np.arange(shape[-2])
    range_x                     = np.arange(shape[-1])
    grid                        = np.array(np.meshgrid(range_y, range_x))
    cells                       = grid.T.reshape(-1, 2)
    length                      = len(cells)
    perrank                     = length // (size - 1)

    test                        = 2

    for yx in range(perrank)[11111: 11111 + test]:
    
        if rank == 0:

            for r in range(1, size):

                r_n             = (size - 1) * yx + (r - 1)
                y               = cells[r_n][0]
                x               = cells[r_n][1]

                arrays_yx       = [array[..., y, x] for array in arrays]

                print(f'Rank {rank} sending cell {r_n} corresponding to')
                print(f'grid indices {x}, {y} to rank {r}.')

                for array in arrays_yx: comm.Send(np.ascontiguousarray(array), dest = r, tag = yx)

                print(f'Rank {rank} succesfully sent data to rank {r}.')
            
            for r in range(1, size):

                r_n             = (size - 1) * yx + (r - 1)
                y               = cells[r_n][0]
                x               = cells[r_n][1]

                print(f'Rank {rank} receiving func {func.__name__} output')
                print(f'from grid indices {x}, {y} to rank {r}.')

                for array in arrays_yx: comm.Recv(return_object, source = r, tag = yx)

        
        if rank != 0:

            r_m                 = (size - 1) * yx + (rank - 1)
            x                   = cells[r_m][0]
            y                   = cells[r_m][1]

            print(f'Rank {rank} receiving cell {r_m} corresponding to')
            print(f'grid indices {x}, {y} from rank 0.')

            for array in arrays_recv: comm.Recv(array, source = 0, tag = yx)

            out_func            = func(arrays_recv, *args, **kwargs)

            comm.Send(out_func, dest = 0, tag = yx)

    print('Done')


def squared(array):

    return array**2


if __name__ == '__main__':

    pixel_wise_w0(squared, ['GPP'], '/p/scratch/cjibg31/jibg3105/data/CLM5EU3/006/join_8d/2010.nc')