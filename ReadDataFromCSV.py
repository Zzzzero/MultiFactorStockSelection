# -*- coding:utf-8 -*-
#
# import basic packages
import numpy as np
import pandas as pd

# this is the parent object of all csv penaled data
# has a name and DataFrame
class ReadDataFromCSV():
    Data = pd.DataFrame()  #DataFrame with str labels
    Name = None
    # class constructor file stored at  "D:/cStrategy/Factor/" by default
    def __init__(self, factorFileName, path="D:/cStrategy/Factor/",):
        # the file path including file name
        self.Name = factorFileName
        path = path+factorFileName+".csv"
        # read the Data Frame
        Data = pd.read_csv(filepath_or_buffer=path)
        # indexing the data
        index = Data[self.Name+"-d"]
        # labeling the dataFrame
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
