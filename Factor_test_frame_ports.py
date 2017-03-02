# -*- coding:utf-8 -*-
# import basic packages
import numpy as np
import pandas as pd
# import project file
import ReadDataFromCSV as rd

class ports_test():
    numOfPorts = None
    datelist = pd.DataFrame().index
    # initilization
    def __init__(self, numberOfPorts ,fdf, rtdf, tradeCapdf):
        self.numOfPorts = int(numberOfPorts)
        # naming the portfolios
        portNames = []
        for i in range(1, self.numOfPorts+1):
            a = "port"+str(i)
            portNames.append(a)
        # creating empty dataframe storing port returns at each return date
        self.dataframe = pd.DataFrame(columns=portNames, index=rtdf.index)
        fdf = fdf.shift(1)
        fdf.drop(fdf.index[0], inplace=True)

        for date in fdf.index:
            ports = self.intoPorts(fdf, date)
            i = 0
            for item in ports:
                self.dataframe.loc[date][portNames[i]] = self.calcPortReturn(item, date, tradeCapdf, rtdf)

                i += 1
    def calcPortReturn (self, port, date, weight, rtdf):
        return None
    def getWeightAtDate (self, tradeCapAtDay):
       return tradeCapAtDay/tradeCapAtDay.sum()
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
        lenth = len(orderedStockCodes)
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






