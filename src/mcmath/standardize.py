import numpy as np

def index_weight(sxi: np.ndarray,
                 weigh_mid: float,
                 weigh_steep: float) -> np.ndarray:

    # Weight SXI with logistic function
    # 10.1175/JHM-D-22-0115.1
    # Calculate logistic weight and set 1 values to np.nan
    
    w = np.where((~np.isnan(sxi) & (sxi < 0)),
                 1 / (1 + (weigh_mid / sxi)**weigh_steep),
                 np.nan)

    return w