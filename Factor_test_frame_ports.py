# -*- coding:utf-8 -*-
# import basic packages
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
# import project file
import ReadDataFromCSV as rd

class Ports_test():
    numOfPorts = None
    # initilization
    def __init__(self, numberOfPorts ,FactorObj, stocksObj, tradeCapObj, neutralized = False):
        fdf = FactorObj.getDataFrame()
        rtdf, _ = stocksObj.calcReturn(stocksObj.Data)
        tradeCapdf = tradeCapObj.getDataFrame()

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
            ports = self.intoPorts(fdf, date, neutralized)
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
    # calculate the weight of stocks using trade capital as numerator on given date
    def getWeightAtDate (self, tradeCapAtDay):
       return tradeCapAtDay/(tradeCapAtDay.sum())
    #  get trade capital at given date
    def getTradeCapAtDate(self, port, tradeCapdf, date):
        return pd.DataFrame(tradeCapdf[port].loc[date])
    #  get the return of a list stocks at given date
    def getReturnAtDate(self, port, rtdf, date):
        return pd.DataFrame(rtdf[port].loc[date])
    # get the industry list of input stocks
    def getIndustry(self):


    # returns the list of list of stock codes
    def intoPorts(self, fdf, date,neutralized):
        if neutralized:
            # neutralize the industrial effect
            print()
        else:
            # not neutralize the industrial effect
            port = []
            # start with the largest
            orderedStockCodes = self.sortFactor(fdf, date)
            lenth = len(orderedStockCodes) / self.numOfPorts
            for i in range(0, self.numOfPorts):
                port.append(orderedStockCodes[i * lenth:(i + 1) * lenth - 1])
        return port
    # sort the factors in same date in descending order
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
    # show the plot of
    def showPlot(self):
        self.cumRtDataFrame.plot()
#####################################################
        # unimplemented method to check the
        # validity of the factor
        # 1. Factor value should corrlated with
        #    ranks of ports corr(Fi,i)
        # 2. Factor corr with port retrun
        # if ARport1>ARportn --> corr>0
        # if ARport1<ARportn --> corr<0
        # 3. the relation should be robust in any
        #    market condition
        #    count(cumrt(port 1)>indexrt)/#allcase
        #    count(cumrt(port n)<indexrt)/#allcase
####################################################
