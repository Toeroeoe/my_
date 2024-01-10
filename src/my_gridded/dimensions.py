
def stack(array_list: list, axis: int = 0):

    """
    Stack arrays of the same shape
    Along a new axis (default 0)
    """

    import numpy as np

    stacked_array       = np.stack(array_list, axis = axis)

    return stacked_array


def select(array, indices, axis):

    """
    Select values from array
    along axis dimension
    """

    import numpy as np

    new_shape           = [1] * array.ndim

    new_shape[axis]     = -1

    indices_dim         = np.reshape(indices, new_shape)

    array_selected      = np.take_along_axis(array, indices_dim, axis = axis)

    return array_selected


def select_by_other(array, array_sel, method: str, axis_select: int, axis_shrink: int):

    """
    Select values from  a 3 or 4 dimenisonal array
    according to method applied on selector array
    The given axis dimension will be shrunk.
    Here assuming constant lat lon dimensions
    at axes -1, -2
    Currently 3d or 4d possible
    """

    import numpy as np
    from my_.gridded.aggregate import apply

    indices             = apply(array_sel, axis_select, method)

    ndim                = array.ndim

    new_axes            = 0 if ndim == 3 else (0, 1) if ndim == 4 else None

    indices_4d          = np.expand_dims(indices, new_axes)

    array_selected      = np.take_along_axis(array, indices_4d, axis = axis_shrink)

    return array_selected


def select_by_self(array, method, axis):

    """
    Select values from array
    The given axis dimension will be shrunk.
    Here assuming constant lat lon dimensions
    at axes -1, -2
    Currently 3d or 4d possible
    """

    import numpy as np
    from my_.gridded.aggregate import apply

    indices             = apply(array, axis, method)

    indices_dim         = np.expand_dims(indices, axis)

    array_selected      = np.take_along_axis(array, indices_dim, axis = axis)

    return array_selected


def slice(array, indices, axis: int):

    """
    Take the same slice for each 1d cell
    across axis dimension
    """

    import numpy as np

    array_sliced        = np.take(array, indices, axis = axis)

    return array_sliced


def select_apply_4d(array, sel_func = select_by_other, sel_func_args = {}, apply_args = {}):

    """
    If there is a fourth dimension
    We select values along given axis
    By selector or by self
    And then we aggregate those by method sel
    and then we apply 
    """

    from my_.gridded.aggregate import apply

    if array.ndim == 4:
         
        var_array_sel   = sel_func(array, **sel_func_args)

        array           = apply(var_array_sel, **apply_args)

    return array


def grid_to_points(lat, lon):

    import numpy as np

    stacked_coords              = np.dstack([lat, lon])
    
    list_points                 = stacked_coords.reshape(-1, 2)

    return list_points