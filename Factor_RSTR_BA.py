import pandas as pd
import numpy as np
import ReadDataFromCSV as rd

data = rd.ReadStockFromCSV("LZ_GPA_QUOTE_TCLOSE")
adj = rd.ReadDataFromCSV("LZ_GPA_CMFTR_CUM_FACTOR")

# div, split backward adjusted price
price = data.Data*adj.Data
# stock return over day t
stockRt = price / price.shift(1)

'''excess returns over risk free rate'''
rf = 0.04
numTradeDays = 252
lag = 21
r = rf / numTradeDays
excessRt = np.log(stockRt)-np.log(1+r)
'''weighted with half_life and rolling window'''
rollingWindow = 504
# exponential weight of half_life
half_life = 126
Factor = pd.DataFrame(index=price.index, columns=price.columns)

def weighted(series, half_life, lag):
    length = len(series)
    expWeight = 0.5 ** (1 / float(half_life))
    data = np.array(range(length+lag-1, lag-1, -1), dtype=float)
    expWeightSeries = float(expWeight)**data
    weighted = pd.Series(data=expWeightSeries, index=series.index)
    weightedExRts = series*weighted
    sum = weightedExRts.sum()
    return sum

'''consider the lag'''
for i, item in enumerate(excessRt.index):
    if i < rollingWindow + lag - 1:
        Factor.loc[item] = np.nan
    else:
        '''the lagged timewindow data'''
        df = excessRt.iloc[:i].tail(rollingWindow + lag).head(rollingWindow+1)
        Factor.loc[item] = df.apply(lambda x: weighted(x, half_life, lag))

dateList = []
for i, item in enumerate(Factor.index):
    datelist = str(item.date()).split("-")
    datestr = datelist[0] + datelist[1] + datelist[2]
    dateList.append(datestr)

Factor.index = dateList

Factor.to_csv("RSTR_1D.csv")



