import pandas as pd
import numpy as np
import talib
from sklearn.decomposition import PCA
import ReadDataFromCSV as rd

volume = rd.ReadFactorFromCSV("LZ_GPA_QUOTE_TVOLUME")
vwap = rd.ReadStockFromCSV("LZ_GPA_QUOTE_AVGPRICE")
open = rd.ReadStockFromCSV("LZ_GPA_QUOTE_TOPEN")
close = rd.ReadStockFromCSV("LZ_GPA_QUOTE_TCLOSE")

intradayDif = (close.Data - open.Data) / open.Data  # intraday market movement detector
vwapData = vwap.calcReturn()  # inbetween day market movement detector
volumeData = volume.Data

# to apply this method, one need to deal with NaN values
pca = PCA(n_components=1)# applyed each row
col = ["1", "2", "3"]
df = pd.DataFrame(columns=col)
# pcindf contains the pc of data in df
pcindf = pd.DataFrame(columns=vwapData.columns, index=vwapData.index)
for date in vwapData.index:  # the index must be the smaller set
    df["1"] = intradayDif.loc[date]
    df["2"] = vwapData.loc[date]
    df["3"] = volumeData.loc[date]
    dt = pd.DataFrame(columns=col)
    # seperate the NaN and values
    for code in df.index:
        if not df.loc[code].isnull().any():
            dt.loc[code] = df.loc[code]
    dtnorm= dt.apply(lambda x: (x-x.mean())/x.std(), axis=0)
    pc = pca.fit_transform(dtnorm)
    # the priciple component in dt
    pcdt = pd.DataFrame(index=dt.index, data=pc)
    # store the coponnet value
    pcindf.loc[date][pcdt.index] = pcdt

pcindf.to_csv("PCin3Fac_1D.csv")





