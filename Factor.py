# -*- coding:utf-8 -*-
#
# import basic packages
import numpy as np
import pandas as pd
# this is the factor object
# has a name and DataFrame
class Factor():
    factor = pd.DataFrame()  #DataFrame with str labels
    factorName = None
    # class constructor file stored at  "D:/cStrategy/Factor/" by default
    def __init__(self, factorFileName, path="D:/cStrategy/Factor/",):
        # the file path including file name
        self.factorName = factorFileName
        path = path+factorFileName+".csv"
        # read the Data Frame
        factor = pd.read_csv(filepath_or_buffer=path)
        # indexing the data
        index = factor[self.factorName+"-d"]
        # labeling the dataFrame
        self.factor = factor.drop(self.factorName+'-d', axis=1).set_index(index.astype(str))
    # getter of the DataFrame of the factor at all avaliable stocks
    def getDataFrame(self):
        return self.factor
    # getter of the Factor name
    def getFactorName(self):
        return self.factorName
    # getter of the Date time of the factor
    def getDateTime(self):
        return self.factor.index
    # getter of certain stock factor data
    # stockCodes could be a array of stockCodes like ["600601.SH","600651.SH"]
    # returns the pd.DataFrame of selected stock factor
    def getFactorForStock(self,stockCodes):
        columnBlock = self.factor[stockCodes]
        return columnBlock
    # select by label: loc, input Dates must be a str array
    def getFactorAtDate(self,Dates):
        return self.factor.loc[Dates]
    # value at stock code and date
    # possible to return NaN if the Dates or stock code are not valid
    def getFactorForStockAtDate(self,stockCodes,Dates):
        return self.factor.loc[Dates][stockCodes]
