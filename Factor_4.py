import pandas as pd
import numpy as np
import ReadDataFromCSV as rd
'''name: alpha_4'''

"""read data"""
low = rd.ReadFactorFromCSV("LZ_GPA_QUOTE_TLOW").Data
# dealing with 0 trade_volume
index = low.index
columns = low.columns
rankLow = low.rank(axis=1)
d = 9

Factor = pd.DataFrame(index=index, columns=columns)
Factor2 = pd.DataFrame(index=index, columns=columns)
Factor3 = pd.DataFrame(index=index, columns=columns)

for i, item in enumerate(rankLow.index):
    if i < 9:
        Factor.loc[item] = np.nan
        Factor2.loc[item] = np.nan
        Factor3.loc[item] = np.nan
    else:
        df = rankLow.loc[:item].tail(d)

        Factor.loc[item] = df.mean()
        Factor2.loc[item] = df.min()
        Factor3.loc[item] = df.max()
        print(item)

dateList = []
for i, item in enumerate(Factor.index):
    datelist = str(item.date()).split("-")
    datestr = datelist[0] + datelist[1] + datelist[2]
    dateList.append(datestr)

Factor.index = dateList
Factor2.index = dateList
Factor3.index = dateList

Factor.to_csv("meanLowRank.csv")
Factor2.to_csv("minLowRank.csv")
Factor3.to_csv("maxLowRank.csv")


