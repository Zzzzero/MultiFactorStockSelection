import pandas as pd
import numpy as np
import ReadDataFromCSV as rd

'''name: alpha_3'''

"""read data"""
open = rd.ReadFactorFromCSV("LZ_GPA_QUOTE_TOPEN").Data
vol = rd.ReadFactorFromCSV("LZ_GPA_QUOTE_TVOLUME").Data
# dealing with 0 trade_volume
logVol = np.log(vol.replace(to_replace=0, value=np.nan))

index = open.index
columns = open.columns

rank1 = open.rank(axis=1)
rank2 = logVol.rank(axis=1)

def correlation(series1, series2):
    df = pd.DataFrame(index=series1.index)
    df[1] = series1
    df[2] = series2
    return df.corr().ix[1, 2]

'''compute signal'''
Factor = pd.DataFrame(index=index, columns=columns)
d = 10
for i, item in enumerate(Factor.index):
    if i < d:
        Factor.loc[item] = np.nan
    else:
        df1 = rank1.loc[:item].tail(d)
        df2 = rank2.loc[:item].tail(d)
        Factor.loc[item] = Factor.apply(lambda x: correlation(df1[x.name], df2[x.name]))

"""store the Factor in correct index"""
dateList = []
for i, item in enumerate(Factor.index):
    datelist = str(item.date()).split("-")
    datestr = datelist[0] + datelist[1] + datelist[2]
    dateList.append(datestr)
Factor.index = dateList

Factor.to_csv("OPENCORRVOL_1D.csv")