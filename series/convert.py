

def cell_to_df(cell, columns, index):

    """
    for 1d or 2d cell data
    """

    import pandas as pd

    df                      = pd.DataFrame(cell, columns = columns, index = index)
    
    return df


def tile_df_to_list(df, n_times):

    list_df                 = list(df)

    list_tiled              = list_df * n_times

    return list_tiled


def tab_to_array(tabular):

    import pandas as pd

    if isinstance(tabular, pd.Series): 
        
        tabular =  tabular.values
    
    if isinstance(tabular, pd.DataFrame): 
            
        tabular =  tabular.values

        tabular = tabular.flatten()

    return tabular


