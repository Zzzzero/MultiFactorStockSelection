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
    def __init__(self, numberOfPorts ,FactorObj, stocksObj, indexObj, tradeCapObj, industry = None, neutralized = False):
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
        self.portAveFactor = pd.DataFrame(columns=portNames, index=fdf.index)
        # filling the data frame of portfolio returns
        for date in rtdf.index:
            ports = self.intoPorts(fdf, date, neutralized, industry)
            i = 0
            for item in ports:
                rtAtDate = self.getReturnAtDate(item, rtdf, date)
                tradeCapAtDate = self.getTradeCapAtDate(item, tradeCapdf, date)
                weightAtDate = self.getWeightAtDate(tradeCapAtDate)
                self.portAveFactor.loc[date][portNames[i]] = fdf[item].loc[date].mean()
                self.rtDataframe.loc[date][portNames[i]] = self.calcRtForPort(weightAtDate, rtAtDate).ix[0, 0]
                i += 1
        # filling the dataframe of portfolio cumulative returns
        self.cumRtDataFrame = (self.rtDataframe+1).cumprod(0)
        indexCumrts = indexObj.cumRts()
        if not (self.cumRtDataFrame.index == indexCumrts.index).any():
            raise ValueError("index value not match")
        self.cumRtDataFrame[indexObj.getIndexCode()] = indexCumrts
        # evaluation the factor

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
    # get the industry list of list of stocks in different industry
    def getIndustryLists(self, industry, date):
        row = industry.loc[date]
        indust = []
        for i in range(1, 24):
            indust.append(row[row == i].index.tolist())
        indust.append(row[np.isnan(row)].index.tolist())
        return indust
    # returns the list of list of stock codes
    def intoPorts (self, fdf, date, neutralized = False, industry = None):
        if neutralized:
            # create  the list of lists
            port = [[] for _ in range(0, self.numOfPorts)]
            industryIndexAtDate = self.getIndustryLists(industry, date)
            for item in industryIndexAtDate:
                orderedStockCodes = self.sortFactor(fdf[item].loc[date])
                lenth = len(orderedStockCodes)/self.numOfPorts
                for i in range(0, self.numOfPorts):
                    port[i].extend(orderedStockCodes[i*lenth:(i+1)*lenth-1])
        else:
            port = []
            # not neutralize the industrial effect
            # start with the largest
            orderedStockCodes = self.sortFactor(fdf.loc[date])
            lenth = len(orderedStockCodes) / self.numOfPorts
            for i in range(0, self.numOfPorts):
                port.append(orderedStockCodes[i * lenth:(i + 1) * lenth - 1])
        return port
    # sort the factors in same date in descending order
    # return the corresponding stock codes
    def sortFactor (self, series):
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

    #  the rank correlation of Factors and returns
    def factorRtCorr(self, method="pearson"):

        portRts = self.rtDataframe  # port returns(over columns)
        portRtValue = portRts.values
        portRtlist = [r for sublist in portRtValue for r in sublist]

        portAveFactor = self.portAveFactor  # the average factor value for each port
        portAveFactorValue = portAveFactor.values
        portAveFactorlist = [f for sublist in portAveFactorValue for f in sublist]

        columns = ["Factor", "Return"]
        relation = pd.DataFrame(columns=columns)
        relation["Factor"] = portAveFactorlist
        relation["Return"] = portRtlist
        # compute the correlation
        return relation.corr(method).ix[0, 1]
    def corr(self):
        portRtrank = self.rtDataframe.rank(axis=1)
        portRtValue = portRtrank.values
        portrtlist = [r for sub in portRtValue for r in sub]
        portFacRank = pd.DataFrame(index= portRtrank.index, columns=portRtrank.columns)
        for date in portRtrank.index:
            rank = self.numOfPorts
            for item in portRtrank.columns:
                portFacRank[item].loc[date] = rank
                rank -= 1
        portFacValue = portFacRank.values
        portFacList = [f for sub in portFacValue for f in sub]

        columns = ["Factor", "Return"]
        relation = pd.DataFrame(columns=columns)
        relation["Factor"] = portFacList
        relation["Return"] = portrtlist

        return relation.corr().ix[1, 0]
    # a method checks the port return with index
    # the best port should constantly beats market
    # the worst port should constantly underperforms the market
    def winLoseOnIndex(self):

        return None
    # the monotonicity of the factor value and port returns
    def aveRts(self):

        return None

