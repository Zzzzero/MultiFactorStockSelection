import pandas as pd
import numpy as np
import ReadDataFromCSV as rd
# (rank((open - (sum(vwap, 10) / 10))) * (-1 * abs(rank((close - vwap)))))
"""read data"""
open = rd.ReadFactorFromCSV("LZ_GPA_QUOTE_TOPEN").Data
close = rd.ReadFactorFromCSV("LZ_GPA_QUOTE_TCLOSE").Data
vwap = rd.ReadFactorFromCSV("LZ_GPA_QUOTE_AVGPRICE").Data

index = open.index
columns = open.columns
"""calc"""
d = 10
part2 = -1 * np.abs((close - vwap).rank(axis=1))
Factor = pd.DataFrame(index=index, columns=columns)
for i, item in enumerate(vwap.index):
    if i < d:
        Factor.loc[item] = np.nan
    else:
        df = vwap.loc[:item].tail(d)
        part1 = (open.loc[item] - df.mean()).rank()
        Factor.loc[item] = part2.loc[item]*part1
        print(item)
dateList = []
for i, item in enumerate(Factor.index):
    datelist = str(item.date()).split("-")
    datestr = datelist[0] + datelist[1] + datelist[2]
    dateList.append(datestr)

Factor.index = dateList
Factor.to_csv("PMStrengh_1D.csv")

