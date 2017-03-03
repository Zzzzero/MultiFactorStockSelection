# -*- coding:utf-8 -*-
# import basic packages
import numpy as np
import pandas as pd
# import project file
import ReadDataFromCSV as rd

class ports_test():
    numOfPorts = None
    # initilization
    def __init__(self, numberOfPorts ,fdf, rtdf, tradeCapdf):
        self.numOfPorts = int(numberOfPorts)
        # naming the portfolios
        portNames = self.namePorts(numberOfPorts)
        # indexing factor with the date on which it generates portfolio returns
        fdf = fdf.shift(1)
        fdf.drop(fdf.index[0], inplace=True)
        # creating empty dataframe storing port returns at each return date
        self.rtDataframe = pd.DataFrame(columns=portNames, index=fdf.index)
        # filling the data frame of portfolio returns
        for date in rtdf.index:
            ports = self.intoPorts(fdf, date)
            i = 0
            for item in ports:
                rtAtDate = self.getReturnAtDate(item, rtdf, date)
                tradeCapAtDate = self.getTradeCapAtDate(item, tradeCapdf, date)
                weightAtDate = self.getWeightAtDate(tradeCapAtDate)
                #print(rtAtDate)
                #print (weightAtDate)
                #print (rtAtDate*weightAtDate)
                self.rtDataframe.loc[date][portNames[i]] = self.calcRtForPort(weightAtDate, rtAtDate).ix[0, 0]
                i += 1
        # filling the dataframe of portfolio cumulative returns
        self.cumRtDataFrame = (self.rtDataframe+1).cumprod(0)
    def calcRtForPort (self, weightAtDate, rtAtDate):
        return (weightAtDate*rtAtDate).sum()
    def getWeightAtDate (self, tradeCapAtDay):
       return tradeCapAtDay/(tradeCapAtDay.sum())
    #  get trade capital at given date
    def getTradeCapAtDate(self, port, tradeCapdf, date):
        return pd.DataFrame(tradeCapdf[port].loc[date])
    def getReturnAtDate(self, port, rtdf, date):
        return pd.DataFrame(rtdf[port].loc[date])
    # returns the list of list of stock codes
    def intoPorts(self, fdf, date):
        port = []
        # start with the largest
        orderedStockCodes = self.sortFactor(fdf, date)
        lenth = len(orderedStockCodes)/self.numOfPorts
        for i in range(0, self.numOfPorts):
            port.append(orderedStockCodes[i*lenth:(i+1)*lenth-1])
        return port
    # sort the factors in same date in ascending order
    # return the corresponding stock codes
    def sortFactor (self, df,date):
        series = df.loc[date]
        # from the biggest to smallest
        sort = series.sort_values(ascending=False)
        return sort.index.tolist()
    # naming the portfolios
    def namePorts (self, numberOfPorts):
        portNames = []
        for i in range(1, numberOfPorts + 1):
            a = "port" + str(i)
            portNames.append(a)
        return portNames






