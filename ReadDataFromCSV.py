# -*- coding:utf-8 -*-
#
# import basic packages
import numpy as np
import pandas as pd
import datetime as dt

# this is the parent object of all csv penaled data
# has a name and DataFrame
# exclude DELISTED STOCKS ONLY
class ReadDataFromCSV (object):
    Data = pd.DataFrame()  #DataFrame with str labels
    Name = None
    # class constructor file stored at  "D:/cStrategy/Factor/" by default
    def __init__(self, factorFileName, path="D:/cStrategy/Factor/"):
        # the file path including file name
        self.Name = factorFileName
        path = path+factorFileName+".csv"
        # read the Data Frame
        Data = pd.read_csv(filepath_or_buffer=path)
        # indexing the data
        index = Data[self.Name+"-d"].astype(str)
        index = pd.to_datetime(index)
        # labeling the dataFrame
        self.Data = Data.drop(self.Name+'-d', axis=1).set_index(index)
    # getter of the DataFrame of the factor at all avaliable stocks
    def getDataFrame(self):
        return self.Data.copy()
    # getter of the Factor name
    def getDataName(self):
        return self.Name.copy()
    # getter of the Date time of the factor
    def getDateTime(self):
        return self.Data.index.copy()
    # getter of certain stock factor data
    # stockCodes could be a array of stockCodes like ["600601.SH","600651.SH"]
    # returns the pd.DataFrame of selected stock factor
    def getDataForStock(self,stockCodes):
        columnBlock = self.Data[stockCodes]
        return columnBlock.copy()
    # select by label: loc, input Dates must be a str array
    def getDataAtDate(self,Dates):
        return self.Data.loc[pd.to_datetime(Dates)].copy()
    # value at stock code and date
    # possible to return NaN if the Dates or stock code are not valid
    def getDataForStockAtDate(self,stockCodes,Dates):
        return self.Data.loc[pd.to_datetime(Dates)][stockCodes].copy()
    # get the data at the end of each month
    def getValueAtMonthEnd(self):
        return self.Data.groupby(pd.TimeGrouper("M")).nth(0).copy()
    # on handing missing data, using interpolate where missing point in between two point
    def handlingMissData(self,method="linear",limit = 28):
        self.Data.interpolate(method=method, limit=limit, axis=0, inplace=True)
    # selecting data after given date
    def setStartTime(self,date):
        self.Data = self.Data.loc[pd.to_datetime(date):]
    # set a test end time
    def setEndTime(self,date):
        self.Data = self.Data.loc[:pd.to_datetime(date)]
    # selecting data valid for last n period
    def selectLatest(self,period):
        self.Data = self.Data.tail(period)
    # drop label if the column contains NAN
    def dropNan(self):
        self.Data = self.Data.dropna(axis=1, how="any")
    # use only stocks with its stock codes in the array codes
    def usePartially (self, codes):
        self.Data = self.Data[codes]
    # return the label of data
    def getlabels (self):
        return self.Data.columns.copy()
    # set the data be at the end of each month
    def setValueAtMonthEnd(self):
        self.Data = self.Data.groupby(pd.TimeGrouper("M")).nth(-1)
    # returns the factor value at provided date
    def prepareFactorAtDate(self, dates):  # dates is in array
        self.Data = self.Data.loc[dates]
# the abstract stock and Factor group
class Read_Stock_Factor (ReadDataFromCSV):
    def __init__(self, factorFileName,
                 path="D:/cStrategy/Factor/",
                 dropDelisted = True):
        super(Read_Stock_Factor, self).__init__(factorFileName, path)
        if dropDelisted:
            # get delisted stocks
            delistStocks = self.getDelisted()
            # droping stocks which are delisted
            self.Data.drop(delistStocks, axis=1, inplace=True)  # drop the delisted stocks
    # get delisted stocks
    def getDelisted(self):
        delist = pd.read_csv(filepath_or_buffer="D:/cStrategy/Factor/LZ_GPA_VAL_A_TCAP.csv")
        delist = delist.tail(2)
        delistFrame = pd.DataFrame(np.isnan(delist.head(1))).drop("LZ_GPA_VAL_A_TCAP-d", axis=1)
        delistStocks = []
        for codes in delistFrame.columns:
            if delistFrame[codes].values[0]:
                delistStocks.append(codes)
        return delistStocks
class ReadStockFromCSV (Read_Stock_Factor):
    #  stocks has a sector index
    def __init__(self, factorFileName,
                 path="D:/cStrategy/Factor/",
                 sectorFileName="LZ_GPA_INDU_ZX",
                 indexPath="D:/cStrategy/Factor/"):
        super(ReadStockFromCSV, self).__init__(factorFileName, path)
        # default path are set to be ZHONGXIN sector
        path2 = indexPath+sectorFileName+".csv"
        self.sector = pd.read_csv(filepath_or_buffer=path2)
        index = self.sector["LZ_GPA_INDU_ZX-t"].astype(str)
        index = pd.to_datetime(index)
        self.sector.set_index(index)
        ##################################################################
        ################BUG HERER!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        ##################################################################
        self.sector = self.sector.drop(sectorFileName+"-t", axis=1, inplace=True)
        self.sector = self.sector.drop(self.getDelisted(), axis=1, inplace=True)
    #  calculating stock return over given period of days
    #  and returns the period begain
    def calcReturn (self, df):
        df = df.copy()
        df = df / df.shift(1) - 1  # calc and return
        pre_date = df.index.delete(-1)
        return df.drop(df.index[0]), pre_date # drop the fist line as it is Nan

# the object Factors
class ReadFactorFromCSV (Read_Stock_Factor):
    # returns standarlized value of each columns in given dataFrame df
    def standarlizedFactors(self, df):
        # this method could be extended with multiple method input
        mean = df.mean()
        std = df.std()
        return (df-mean)/std
    #  de-extreme value of data in columns
    def deExtremum (self,df):
        ################
        # unimplemented#
        ################
        return df
# the object indexs
class IndexFromCSV(ReadDataFromCSV):
    def __init__(self, indexName = "000300.SH",
                 factorFileName="LZ_GPA_INDXQUOTE_CLOSE",
                 path="D:/cStrategy/Factor/"):
        super(IndexFromCSV, self).__init__(factorFileName, path)
        self.Data = self.Data[indexName]
    def calcReturn (self, df):
        df = df.copy()
        df = df / df.shift(1) - 1  # calc and return
        pre_date = df.index.delete(-1)  # return the period start date
        return df.drop(df.index[0]), pre_date

# calc return premium, df and series must be the dataframe and series
# of return over the same period on stocks and index
# input stock return df, index return series
# out put retrun premium
def rtOverIndex(df, series):
    rp = pd.DataFrame(index=df.index)
    rp = df.sub(series, axis=0)
    return rp