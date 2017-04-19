import pandas as pd
import numpy as np
import statsmodels.api as sm
import ReadDataFromCSV as rd

data = rd.ReadStockFromCSV("LZ_GPA_QUOTE_TCLOSE")
adj = rd.ReadDataFromCSV("LZ_GPA_CMFTR_CUM_FACTOR")
market =rd.IndexFromCSV("000001.SH")

# div, split backward adjusted price
price = data.Data*adj.Data
# stock return over day t
stockRt = price / price.shift(1) - 1
# market rt
benchRt = market.calcReturn()
rf = 0.04 / 252
excessRt = stockRt - rf
excessIndRt = benchRt - rf

'''reg'''
half_life = 63
trialing = 252
naTol = trialing / 3

weight = (0.5**(1/float(half_life)))**np.array(range(trialing, 0, -1))
def ols(Y, X, naTol):
    '''check number of nan'''
    df = pd.DataFrame(index=X.index)
    df["X"] = X
    df["Y"] = Y
    num = df.isnull().any(axis=1).sum()
    if num > naTol:
        return np.nan
    else:
        x = sm.add_constant(X)
        model = sm.OLS(Y, x, missing='drop')
        results = model.fit()
        return results.params.iloc[1]
Factor = pd.DataFrame(index=price.index, columns=price.columns)

for i, item in enumerate(Factor.index):
    if i < trialing:
        Factor.loc[item] = np.nan
    else:
        X = excessIndRt.loc[:item].tail(trialing)
        exWeight = pd.Series(data=weight, index=X.index)
        Y = excessRt.loc[:item].tail(trialing)
        Factor.loc[item] = Y.apply(lambda y: ols(y*exWeight, X*exWeight, naTol))

dateList = []
for i, item in enumerate(Factor.index):
    datelist = str(item.date()).split("-")
    datestr = datelist[0] + datelist[1] + datelist[2]
    dateList.append(datestr)

Factor.index = dateList

Factor.to_csv("WBeta_1D.csv")



