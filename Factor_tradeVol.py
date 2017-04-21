import pandas as pd
import numpy as np
import statsmodels.api as sm
import ReadDataFromCSV as rd

data = rd.ReadFactorFromCSV("LZ_GPA_QUOTE_TVOLUME")
vol = data.Data
'''the sense vol~sigma'''
half_life = 63
trialing = 252
naTol = trialing / 3

weight = (0.5**(1/float(half_life)))**np.array(range(trialing, 0, -1))
weight = weight/weight.sum()

Factor = pd.DataFrame(index=vol.index, columns=vol.columns)

for i, item in enumerate(Factor.index):
    if i < trialing:
        Factor.loc[item] = np.nan
    else:
        df = vol.loc[:item].tail(trialing)
        exWeight = pd.Series(data=weight, index=df.index)
        Factor.loc[item] = df.apply(lambda x: (x*exWeight).sum())

dateList = []
for i, item in enumerate(Factor.index):
    datelist = str(item.date()).split("-")
    datestr = datelist[0] + datelist[1] + datelist[2]
    dateList.append(datestr)

Factor.index = dateList

Factor.to_csv("WVol_1D.csv")