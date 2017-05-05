import pandas as pd
import numpy as np
import ReadDataFromCSV as rd
#((adv20 < volume) ? ((-1 * ts_rank(abs(delta(close, 7)), 60)) * sign(delta(close, 7))) : (-1 * 1))

"""read data"""
vol = rd.ReadFactorFromCSV("LZ_GPA_QUOTE_TVOLUME").Data
closeObj = rd.ReadFactorFromCSV("LZ_GPA_QUOTE_TCLOSE")
index = closeObj.strIndex
close = closeObj.Data




