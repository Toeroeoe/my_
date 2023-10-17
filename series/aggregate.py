

def concat(dfs: list = [], join: str = 'outer', axis: int = 1, sort: bool = True):

    import pandas as pd

    if axis == 1:

        dfs                 = add_missing_column_levels(dfs)

    df                      = pd.concat(dfs, join = join, axis = axis)

    if sort: 

        df                  = df.sort_index(axis = axis)

    return df


def add_missing_column_levels(dfs):

    from my_.series.group import add_level_to_multi_columns
    
    nlevels                 = [df.columns.nlevels for df in dfs]

    if nlevels.count(nlevels[0]) == len(nlevels): return dfs

    max_levels              = max(nlevels)

    i_max_levels            = nlevels.index(max_levels)

    max_columns             = set(dfs[i_max_levels].columns.names)

    new_dfs                 = []

    for df in dfs:

        diff_columns        = set(max_columns).difference(set(df.columns.names))

        for missing_level in diff_columns:

            new_level       = ['-1'] * len(df.columns)

            new_loc         = len(df.columns.names)

            df              = add_level_to_multi_columns(df, new_loc, missing_level, new_level)

        new_dfs.append(df)

    return new_dfs

            

def mask(df, masker, value, skip_mask_NA = True):

    import pandas as pd

    if skip_mask_NA:

        df_masked           = df.where(masker.values >= value, axis = 0)
    
    elif not skip_mask_NA:

        df_masked           = df.where(((masker.values >= value) | (masker.values == pd.NA)), axis = 0)

    return df_masked



def apply(df, method):


    import pandas as pd

    # find the method in numpy attributes
    method_pd               = getattr(pd, method)

    df_new                  = df.agg(method_pd, skipna = False)

    return df_new


def column_wise(df, ffunc):

    import pandas as pd
    from itertools import product

    columns                 = df.columns

    df_out                  = pd.DataFrame(columns = columns, index = columns)

    iterator                = product(columns, columns)

    for col1, col2 in iterator:

        col1_v              = df[col1]

        col2_v              = df[col2]

        df_out.loc[col1, col2] = ffunc(col1_v, col2_v)

    return df_out


def single_column_wise(df, column: str, ffunc):

    print('haha')