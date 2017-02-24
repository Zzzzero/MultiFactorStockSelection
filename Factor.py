# -*- coding:utf-8 -*-
#
# import basic packages
import numpy as np
import pandas as pd
# this is the factor object
# has a name and DataFrame
class Factor():
    factor = pd.DataFrame()
    factorName = None
    def __init__(self, factorFileName, path="D:/cStrategy/Factor/",):
        # the file path including file name
        self.factorName = factorFileName
        path = path+factorFileName+".csv"
        self.factor = pd.read_csv(filepath_or_buffer=path)
    # getter of the DataFrame
    def getDataFrame(self):
        return self.factor
    # getter of the Factor name
    def getFactorName(self):
        return self.factorName
    # getter of the Date time of the factor
    def getDateTime(self):
        return self.factor[self.factorName+"-d"]
    # get stock
    # more attr may be added in the feature e.g the postion of NaN


