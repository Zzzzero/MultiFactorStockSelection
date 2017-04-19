import pandas as pd
import numpy as np
import talib
from sklearn.decomposition import PCA
from joblib import delayed, Parallel
import multiprocessing
import ReadDataFromCSV as rd

def readData():
    start = "20161101"
    end = "20170101"
    volume = rd.ReadFactorFromCSV("LZ_GPA_QUOTE_TVOLUME")
    vwap = rd.ReadStockFromCSV("LZ_GPA_QUOTE_AVGPRICE")
    open = rd.ReadStockFromCSV("LZ_GPA_QUOTE_TOPEN")
    close = rd.ReadStockFromCSV("LZ_GPA_QUOTE_TCLOSE")

    volume.setStartTime(start)
    volume.setEndTime(end)
    vwap.setStartTime(start)
    vwap.setEndTime(end)
    open.setStartTime(start)
    open.setEndTime(end)
    close.setStartTime(start)
    close.setEndTime(end)

    return volume, vwap, open, close
def crossSectionalPCA(date, intradayDif, vwapData, volumeData):
    col = ["1", "2", "3"]
    df = pd.DataFrame(columns=col)
    # set pca
    pca = PCA(n_components=1)  # applyed each row
    df["1"] = intradayDif.loc[date]
    df["2"] = vwapData.loc[date]
    df["3"] = volumeData.loc[date]
    dt = pd.DataFrame(index=col)
    for code in df.index:
        if not df.loc[code].isnull().any():
            dt[code] = df.loc[code]
    dtnorm= dt.apply(lambda x: (x-x.mean())/x.std(), axis=1)
    pc = pca.fit(dtnorm).components_
    # the priciple component in dt
    pcdt= pd.DataFrame(columns=dt.columns, data=pc, index=[date])
    pcindf = pd.DataFrame(columns=df.index, index=[date])
    pcindf[pcdt.columns] = pcdt
    # pcdt is a dataframe with index = date, columns=code
    return pcindf
def main():
    volume, vwap, open, close = readData()
    # construct variables
    intradayDif = (close.Data - open.Data) / open.Data  # intraday market movement detector
    vwapData = vwap.calcReturn()  # inbetween day market movement detector
    volumeData = volume.Data

    # df contains the pc of data in df
    df = pd.DataFrame(columns=vwapData.columns, index=vwapData.index)

    pcindflist = Parallel(n_jobs=-1)(delayed(crossSectionalPCA)(date, intradayDif, vwapData, volumeData)
                                     for date in vwapData.index)

    for i, date in enumerate(vwapData.index):
        df.loc[date][pcindflist[i]] = pcindflist[i].loc[date]
    return df
if __name__ == "__main__":
    main()
