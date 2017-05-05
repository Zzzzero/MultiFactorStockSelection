import pandas as pd
import numpy as np
import ReadDataFromCSV as rd

'''name: alpha_6(-1 * correlation(open, volume, 10))'''

"""read data"""
openObj = rd.ReadFactorFromCSV("LZ_GPA_QUOTE_TOPEN")
open = openObj.Data
index = openObj.strIndex
vol = rd.ReadFactorFromCSV("LZ_GPA_QUOTE_TVOLUME").Data
vol = vol.replace(to_replace=0, value=np.nan)
"""calc"""
"""func"""
def correlation(series1, series2, naTol):
    df = pd.DataFrame(index=series1.index)
    df[1] = series1
    df[2] = series2
    if df.isnull().sum().sum() / 2 > naTol:
        return np.nan
    else:
        return df.corr().ix[1, 2]
d = 10
Factor = pd.DataFrame(index=open.index, columns=open.columns)
for i, item in enumerate(Factor.index):
    if i < d:
        Factor.loc[item] = np.nan
    else:
        ropen = open.loc[:item].tail(d)
        rvol = vol.loc[:item].tail(d)
        Factor.loc[item] = Factor.apply(lambda x: correlation(ropen[x.name], rvol[x.name], 3))
        print(item)

Factor.index = index
Factor.to_csv("OpenVolCo_1D.csv")


