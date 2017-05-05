import pandas as pd
import numpy as np
import ReadDataFromCSV as rd
#'''name: 8  (-1 * rank(((sum(open, 5) * sum(returns, 5)) - delay((sum(open, 5) * sum(returns, 5)), 10)))) '''
"""read data"""
open = rd.ReadFactorFromCSV("LZ_GPA_QUOTE_TOPEN").Data
closeObj = rd.ReadFactorFromCSV("LZ_GPA_QUOTE_TCLOSE")
close = closeObj.Data
index = closeObj.strIndex

"calc"
rts = close / close.shift(1) -1
Factor = pd.DataFrame(index=close.index, columns=close.columns)

opdf = pd.DataFrame(index=close.index, columns=close.columns)
rtdf = pd.DataFrame(index=close.index, columns=close.columns)
d = 5
d2 = 10
for i, item in enumerate(opdf.index):
    if i < d:
        opdf.loc[item] = np.nan
        rtdf.loc[item] = np.nan
    else:
        opdf.loc[item] = open.loc[:item].tail(d).sum()
        rtdf.loc[item] = rts.loc[:item].tail(d).sum()

for i, item in enumerate(Factor.index):
    if i < (d + d2):
        Factor.loc[item] = np.nan
    else:
        p1 = opdf.loc[item] * rtdf.loc[item]
        p2 = opdf.shift(d2).loc[item] * rtdf.shift(d2).loc[item]
        Factor.loc[item] = -1 * (p1 - p2).rank()

Factor.index = index
Factor.to_csv("5dayPrtDif_1D.csv")
