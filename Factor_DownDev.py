import pandas as pd
import numpy as np
import statsmodels.api as sm
import ReadDataFromCSV as rd
'''downside deviation'''
data = rd.ReadStockFromCSV("LZ_GPA_QUOTE_TCLOSE")
adj = rd.ReadDataFromCSV("LZ_GPA_CMFTR_CUM_FACTOR")

# div, split backward adjusted price
price = data.Data*adj.Data
# stock return over day t
stockRt = price / price.shift(1) - 1

''' calc '''
half_life = 63
trialing = 252
naTol = trialing / 3
rf = 0.04
trf = 0.04/252

Factordr = pd.DataFrame(index=price.index, columns=price.columns)
Factorsor = pd.DataFrame(index=price.index, columns=price.columns)
for i, item in enumerate(stockRt.index):
    if i < trialing - 1:
        Factordr.loc[item] = np.nan
        Factorsor.loc[item] = np.nan
    else:
        df = stockRt.iloc[:i].tail(trialing)
        naIndex = df.isnull().sum() > naTol

        down = df < trf
        downside2 = df[down]**2

        dr = np.sqrt(downside2.sum() / float(trialing))
        meandiv = df.mean() - trf

        Factordr.loc[item] = dr
        Factordr.loc[item][naIndex] = np.nan
        Factorsor.loc[item] = meandiv / dr
        Factorsor.loc[item][naIndex] = np.nan

dateList = []
for i, item in enumerate(Factordr.index):
    datelist = str(item.date()).split("-")
    datestr = datelist[0] + datelist[1] + datelist[2]
    dateList.append(datestr)

Factordr.index = dateList
Factorsor.index = dateList

Factordr.to_csv("DR_1D.csv")
Factorsor.to_csv("SORDALIY_1D.csv")




