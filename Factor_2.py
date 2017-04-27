import pandas as pd
import numpy as np
import ReadDataFromCSV as rd

'''name: alpha_2'''

"""read data"""
close = rd.ReadFactorFromCSV("LZ_GPA_QUOTE_TCLOSE").Data
open = rd.ReadFactorFromCSV("LZ_GPA_QUOTE_TOPEN").Data
vol = rd.ReadFactorFromCSV("LZ_GPA_QUOTE_TVOLUME").Data
# dealing with 0 trade_volume
logVol = np.log(vol.replace(to_replace=0, value=np.nan))

index = close.index
columns = close.columns

delay = 2
rank1 = ((close - open) / open).rank(axis=1)
delta = logVol - logVol.shift(delay)
rank2 = delta.rank(axis=1)

def correlation(series1, series2, naTol):
    df = pd.DataFrame(index=series1.index)
    df[1] = series1
    df[2] = series2

    if df.isnull().sum().sum() / 2 > naTol:
        return np.nan
    else:
        return df.corr().ix[1, 2]

'''compute signal'''
Factor = pd.DataFrame(index=index, columns=columns)
d = 6
for i, item in enumerate(Factor.index):
    if i < d:
        Factor.loc[item] = np.nan
    else:
        df1 = rank1.loc[:item].tail(d)
        df2 = rank2.loc[:item].tail(d)
        Factor.loc[item] = Factor.apply(lambda x: correlation(df1[x.name], df2[x.name], naTol=d / 3))

"""store the Factor in correct index"""
dateList = []
for i, item in enumerate(Factor.index):
    datelist = str(item.date()).split("-")
    datestr = datelist[0] + datelist[1] + datelist[2]
    dateList.append(datestr)
Factor.index = dateList

Factor.to_csv("RTCORRVOL_1D.csv")
