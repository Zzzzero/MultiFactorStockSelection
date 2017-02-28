# -*- coding:utf-8 -*-
#
# import basic packages
import numpy as np
import pandas as pd

# this is the parent object of all csv penaled data
# has a name and DataFrame
# exclude DELISTED STOCKS ONLY
class ReadDataFromCSV():
    Data = pd.DataFrame()  #DataFrame with str labels
    Name = None
    # class constructor file stored at  "D:/cStrategy/Factor/" by default
    def __init__(self, factorFileName, path="D:/cStrategy/Factor/"):
        # the file path including file name
        self.Name = factorFileName
        path = path+factorFileName+".csv"
        # read the Data Frame
        Data = pd.read_csv(filepath_or_buffer=path)
        # getting stock codes which are delisted
        delistStocks = self.getDelisted()
        # indexing the data
        index = Data[self.Name+"-d"]
        # labeling the dataFrame
        self.Data = Data.drop(delistStocks, axis=1, inplace=True)  # drop the delisted stocks
        self.Data = Data.drop(self.Name+'-d', axis=1).set_index(index.astype(str))
    # getter of the DataFrame of the factor at all avaliable stocks
    def getDataFrame(self):
        return self.Data
    # getter of the Factor name
    def getDataName(self):
        return self.Name
    # getter of the Date time of the factor
    def getDateTime(self):
        return self.Data.index
    # getter of certain stock factor data
    # stockCodes could be a array of stockCodes like ["600601.SH","600651.SH"]
    # returns the pd.DataFrame of selected stock factor
    def getDataForStock(self,stockCodes):
        columnBlock = self.Data[stockCodes]
        return columnBlock
    # select by label: loc, input Dates must be a str array
    def getDataAtDate(self,Dates):
        return self.Data.loc[Dates]
    # value at stock code and date
    # possible to return NaN if the Dates or stock code are not valid
    def getDataForStockAtDate(self,stockCodes,Dates):
        return self.Data.loc[Dates][stockCodes]
    # get delisted stocks
    def getDelisted(self):
        # filting the delist stocks
        delist = pd.read_csv(filepath_or_buffer="D:/cStrategy/Factor/LZ_GPA_VAL_A_TCAP.csv")
        delistFrame = pd.DataFrame(np.isnan(delist.tail(1))).drop("LZ_GPA_VAL_A_TCAP-d", axis=1)
        delistStocks = []
        for codes in delistFrame.columns:
            if delistFrame[codes].values[0]:
                delistStocks.append(codes)
        return delistStocks
    # on handing missing data, using interpolate where missing point in between two point
    def handlingMissData(self,method="linear",limit = 28):
        self.Data.interpolate(method=method, limit=limit, axis=0, inplace=True)
    # selecting data after given date
    def setStartTime(self,date):
        self.Data = self.Data.loc[str(date):]
    # selecting data valid for last n period
    def selectLatest(self,period):
        self.Data = self.Data.tail(period)
# this is the child object of stock price data
class readStockFromCSV (ReadDataFromCSV):
    #  calculating stock return over given period of days
    def CalcReturn(self, period=1):
        # creating a empty pd DataFrame
        df = self.Data.ix[0::period]  # retrieve every period of rows
        return df / df.shift(1) - 1  # calc and return
