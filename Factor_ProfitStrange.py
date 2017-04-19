import pandas as pd
import numpy as np
import ReadDataFromCSV as rd

data = rd.ReadStockFromCSV("LZ_GPA_QUOTE_TCLOSE")
adj = rd.ReadDataFromCSV("LZ_GPA_CMFTR_CUM_FACTOR")

# div, split backward adjusted price
price = data.Data*adj.Data
# stock return over day t
stockRt = price / price.shift(1)
'''excess rts'''

rf = 0.04
numTradeDays = 252
r = rf / numTradeDays
excessRt = np.log(stockRt)-np.log(1+r)
rollingWindow = 60
half_life = 20

def calc(series):
    absSum = series.abs().sum()
    sum = series.sum()
    return float(sum) / float(absSum)
def calcWeighted(series, half_life):
    lenth = len(series)
    expWight = 0.5**(1/float(half_life))
    data = np.array(range(lenth, 0, -1), dtype=float)
    weight = expWight**data

    weighted = pd.Series(data=weight, index=series.index)
    wtRt = series*weighted

    return calc(wtRt)

'''calc the factor'''
Factor = pd.DataFrame(index=price.index, columns=price.columns)
FactorWeighted = pd.DataFrame(index=price.index, columns=price.columns)

for i, item in enumerate(excessRt.index):
    if i < rollingWindow - 1:
        Factor.loc[item] = np.nan
        FactorWeighted.loc[item] = np.nan
    else:
        '''the lagged timewindow data'''
        df = excessRt.iloc[:i].tail(rollingWindow)
        Factor.loc[item] = df.apply(lambda x: calc(x))
        FactorWeighted.loc[item] = df.apply(lambda x: calcWeighted(x, half_life))

dateList = []
for i, item in enumerate(Factor.index):
    datelist = str(item.date()).split("-")
    datestr = datelist[0] + datelist[1] + datelist[2]
    dateList.append(datestr)

Factor.index = dateList
FactorWeighted.index = dateList

Factor.to_csv("ProfitStrangth_1D.csv")
FactorWeighted.to_csv("WeightedProfitStrangth_1D.csv")
