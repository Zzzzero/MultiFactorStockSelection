import pandas as pd
import numpy as np
import ReadDataFromCSV as rd
#((adv20 < volume) ? ((-1 * ts_rank(abs(delta(close, 7)), 60)) * sign(delta(close, 7))) : (-1 * 1))

"""read data"""
vol = rd.ReadFactorFromCSV("LZ_GPA_QUOTE_TVOLUME").Data
closeObj = rd.ReadFactorFromCSV("LZ_GPA_QUOTE_TCLOSE")
#adj = rd.ReadFactorFromCSV("LZ_GPA_CMFTR_CUM_FACTOR").Data
index = closeObj.strIndex
close = closeObj.Data
def value(series, flag):
    print(series.name)
    if flag:
        return -1*(np.abs(series).rank())[-1] * np.sign(series)[-1]
    elif not flag:
        return -1
    else:
        return np.nan
dv = vol * close
tsd = 60
deltad = 7
advd = 20
delayColse = close.shift(deltad)

Factor = pd.DataFrame(index=vol.index, columns=vol.columns)
for i, item in enumerate(Factor.index):
    if i < tsd:
        Factor.loc[item] = np.nan
    else:
        dv = close.loc[:item].tail(advd).mean()
        dayvol = vol.loc[item]
        binaryDv1 = dv < dayvol
        binaryDv2 = ~(dv > dayvol)
        corBinary = binaryDv1.loc[binaryDv1 == binaryDv2]

        df = delayColse.loc[:item].tail(tsd)
        for i,item in enumerate(df.columns):
            print(df[item].name)
        Factor.loc[item] = df.apply(lambda x: value(x, corBinary[x.name]))

Factor.index = index

Factor.to_csv("tsDVrank_1D.csv")


