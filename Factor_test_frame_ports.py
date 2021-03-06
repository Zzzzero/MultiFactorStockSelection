# -*- coding:utf-8 -*-
# import basic packages
import numpy as np
import pandas as pd
import statsmodels as stm
import matplotlib.pyplot as plt
#  excle editing tool
from joblib import delayed, Parallel
import dill
import datetime as dt
# import project file
import ReadDataFromCSV as rd

class Ports_test():
    numOfPorts = None
    # initilization
    def __init__(self, numberOfPorts,delayPeriod,FactorObj, stocksObj, indexObj, tradeCapObj, industry = None, neutralized = False):

        # self instance variables
        self.factorName = FactorObj.getDataName()
        self.rtDataframe = None
        self.portAveFactor = None
        self.cumRtDataFrame = None
        self.numOfPorts = int(numberOfPorts)
        self.indexObj = indexObj
        self.delayPeriod = delayPeriod

        # copys of data we need to manipulate
        rtdf = stocksObj.calcReturn(method="F")
        tradeCapdf = tradeCapObj.getDataFrame()
        # delay the factor by defined period
        fdf = self.delay(FactorObj.Data, self.delayPeriod)

        # initilize the self instance variables
        self.initilize(rtdf, fdf, tradeCapdf, neutralized, industry)
    if __name__ == "__main__":
        __init__()
# section 1, run the simulation
    # initilize the self instance variables
    def initilize(self, rtdf, fdf, tradeCapdf, neutralized, industry):

        portNames = self.namePorts(self.numOfPorts)
        self.rtDataframe = pd.DataFrame(columns=portNames, index=fdf.index)
        self.portAveFactor = pd.DataFrame(columns=portNames, index=fdf.index)
        # filling the data frame of portfolio returns
        #Parallel(n_jobs=-1)(
         #   delayed(self.intoPortsPerDay)(date, fdf, rtdf, tradeCapdf, portNames,
          #                                neutralized, industry) for date in fdf.index)
        for date in fdf.index:
            self.intoPortsPerDay(date, fdf, rtdf, tradeCapdf, portNames, neutralized, industry)
        # filling the dataframe of portfolio cumulative returns
        self.cumRtDataFrame = (self.rtDataframe + 1).cumprod(0)
    def intoPortsPerDay(self, date, fdf, rtdf, tradeCapdf, portNames, neutralized, industry):
        ports = self.intoPorts(fdf, date, neutralized, industry)
        i = 0
        for item in ports:
            rtAtDate = self.getReturnAtDate(item, rtdf, date)
            tradeCapAtDate = self.getTradeCapAtDate(item, tradeCapdf, date)
            weightAtDate = self.getWeightAtDate(tradeCapAtDate)
            self.portAveFactor.loc[date][portNames[i]] = fdf[item].loc[date].mean()
            self.rtDataframe.loc[date][portNames[i]] = self.calcRtForPort(weightAtDate, rtAtDate).ix[0, 0]
            i += 1
    # setting delay of factor to make alpha(n), to test the (Rtm , Fac(m-n)) pair
    def delay(self,df, numOfPeriod=1):
        return df.shift(numOfPeriod).drop(df.index[:numOfPeriod])
    # calculate the trade capital weighted return of each port
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
        for i in range(1, 30):
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
                deNa = fdf[item].loc[date].dropna()  # drop nan value label
                orderedStockCodes = self.sortFactor(deNa)
                lenth = len(orderedStockCodes)/self.numOfPorts
                for i in range(0, self.numOfPorts):
                    port[i].extend(orderedStockCodes[i*lenth:(i+1)*lenth-1])
        else:
            port = []
            # not neutralize the industrial effect
            # start with the largest
            deNa = fdf.loc[date].dropna()
            orderedStockCodes = self.sortFactor(deNa)
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
    # this returns the excess return of ports over index in each period
    def excessRts(self):
        df = self.indexObj.calcReturn()
        return self.excessOverIndex(self.rtDataframe, df)
    # this gives the return or cumrt over index
    def excessOverIndex(self, df, indexdf):
        df = df.copy()
        for item in df.columns[0:self.numOfPorts]:
            df[item] = df[item] - indexdf
        return df.astype(float)
# section 2 , the graphs
    # show the plot of the cumulative reuturns of each ports
    def showCumRtPlot(self):
        df = self.cumRtDataFrame.copy()
        df[self.indexObj.getIndexCode()] = self.indexObj.cumRts()
        return df.plot()
    # show the scatter plot of port1 - port5 pair
    def port1ToNScatterExRts(self):
        df = self.excessRts()
        return df.ix[:, [0, self.numOfPorts-1]].plot(kind="scatter", x=df.columns[0], y=df.columns[self.numOfPorts-1])
# section 3, the evaluation of chosen factor
    # the correlation
    def corrPortsExRts(self, method="pearson"):
        df = self.excessRts()
        return df.corr(method)
    def factorExRtCorr(self, method="pearson"):

        portExRts = self.excessRts()  # port excess returns over index
        portRtValue = portExRts.values
        portRtlist = [r for sublist in portRtValue for r in sublist]

        portAveFactor = self.portAveFactor  # the average factor value for each port
        portAveFactorValue = portAveFactor.values
        portAveFactorlist = [f for sublist in portAveFactorValue for f in sublist]

        columns = ["Factor", "Return"]
        relation = pd.DataFrame(columns=columns)
        relation["Factor"] = portAveFactorlist
        relation["Excess Return"] = portRtlist
        # compute the correlation
        return relation.corr(method).ix[0, 1]
    def corr(self):
        portExRtrank = self.excessRts().rank(axis=1)
        portExRtValue = portExRtrank.values
        portrtlist = [r for sub in portExRtValue for r in sub]
        portFacRank = pd.DataFrame(index=portExRtrank.index, columns=portExRtrank.columns)
        for date in portExRtrank.index:
            rank = self.numOfPorts
            for item in portExRtrank.columns:
                portFacRank[item].loc[date] = rank
                rank -= 1
        portFacValue = portFacRank.values
        portFacList = [f for sub in portFacValue for f in sub]

        columns = ["Factor", "Return"]
        relation = pd.DataFrame(columns=columns)
        relation["Factor"] = portFacList
        relation["Return"] = portrtlist

        return relation.corr().ix[1, 0]
    # decide the direction of the influence of the factor
    def directOfInfluByAveRt(self):
        df = self.aveRtRanks()
        if df[0] > df[-1]:
            return 1
        elif df[0] == df[-1]:
            return 0
        else:
            return -1
    def directOfInfluByCorr(self):
        corr = self.factorExRtCorr()
        if corr > 0:
            return 1
        elif corr == 0:
            return 0
        else:
            return -1
    def direction(self):
        if self.directOfInfluByAveRt() == self.directOfInfluByCorr():
            direction = self.directOfInfluByAveRt()
        else:
            direction = 0
        return direction
    # the monotonicity of the factor value and port returns
    def aveRtRanks (self):
        return self.rtDataframe.mean().rank()
    # decide if the how good is the monotonicity,
    # good results attained as the value close to zero
    def monotonicity (self):
        monotonicity = -1  # initial value neg to avoid error usage
        # the poorest monotonicity if monotonicity can exam
        maxM = 0
        for i in range(1, self.numOfPorts+1):
            maxM += (i-(self.numOfPorts+1-i))**2

        if self.directOfInfluByAveRt() == self.directOfInfluByCorr():
            if self.directOfInfluByCorr() == 1:  # postive influence
                arr = np.array(range(self.numOfPorts, 0, -1))
                monotonicity = ((self.aveRtRanks()-arr).apply(np.square)).sum()
            elif self.directOfInfluByCorr() == -1:  # neg influence
                arr = np.array(range(1, self.numOfPorts+1, 1))
                monotonicity = ((self.aveRtRanks()-arr).apply(np.square)).sum()
            else:
                monotonicity == np.inf
        else:
            monotonicity = np.inf
        return monotonicity / maxM
    # a method checks the port cumulative return with index
    # the best port should constantly beats market
    # the worst port should constantly underperforms the market
    def cumRtwinLoseOnIndex(self):
        ports = self.excessOverIndex(self.cumRtDataFrame, self.indexObj.cumRts())
        lenth = len(ports)
        win = (ports > 0).sum() / lenth
        lose = (ports < 0).sum() / lenth
        return win, lose
    # a method check port excess return with idnex
    def ExRtwinLoseOnIndex(self):
        ports = self.excessRts()
        lenth = len(ports)
        win = (ports > 0).sum() / lenth
        lose = (ports < 0).sum() / lenth
        return win, lose
    def relativeWinRatio(self):
        ports, _ = self.ExRtwinLoseOnIndex()
        if self.direction() == 1:
            return ports[0]/ports[self.numOfPorts-1]  # port1 rt / portN rt
        elif self.direction() == -1:
            return ports[self.numOfPorts-1]/ports[0]
        else:
            return -1
    def relativeLoseRatio(self):
        _, ports = self.ExRtwinLoseOnIndex()
        if self.direction() == -1:
            return ports[0] / ports[self.numOfPorts - 1]  # port1 rt / portN rt
        elif self.direction() == 1:
            return ports[self.numOfPorts - 1] / ports[0]
        else:
            return -1
    # the evaluation result
    def result(self):
        columns = ["test_time",
                   "test_start",
                   "test_end",
                   "direction",
                   "port_excess_rts_corr",
                   "relative_win_ratio",
                   "relative_lose_ratio",
                   "monotonicity",
                   "IC"]
        result = pd.DataFrame(columns=columns, index=[self.factorName])
        # the factor info
        result["test_time"] = str(dt.datetime.now())
        result["test_start"] = str(self.rtDataframe.index[0])
        result["test_end"] = str(self.rtDataframe.index[self.numOfPorts-1])
        # the related test results
        result["direction"] = self.direction()
        result["port_excess_rts_corr"] = self.corrPortsExRts().ix[0, self.numOfPorts-1]
        result["relative_win_ratio"] = self.relativeWinRatio()
        result["relative_lose_ratio"] = self.relativeWinRatio()
        result["monotonicity"] = self.monotonicity()
        result["IC"] = self.factorExRtCorr()

        return result
#  writing a test report to a given path
    def report(self, filepath="C:/Users/LZJF_02/Desktop/test.csv"):
        #  read the data stored in file
        data = pd.read_csv(filepath_or_buffer=filepath)
        index = data.ix[:, 0].astype(str)
        data = data.drop(data.columns[0], axis=1).set_index(index)
        #  the new output of this test
        newdata = self.result()
        # merge the data frame
        if data.index.map(lambda x: x == newdata.index).any():
            # the factor alread tested before, then replace it
            data.loc[newdata.index[0]] = newdata.values[0]
        else:
            # the factor are not previously tested
            data.loc[newdata.index[0]] = newdata.values[0]
        # save the updated info in csv
        data.to_csv(filepath)





