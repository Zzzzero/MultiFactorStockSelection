import numpy as np
def calc(close, cumfac, month):
    facClose = close * cumfac
    prePad = np.full((month, facClose.shape[1]), np.nan)
    return facClose / np.r_[prePad,facClose[:-month]] -1
