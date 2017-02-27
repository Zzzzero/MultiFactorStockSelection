import pandas as pd
import ReadDataFromCSV as rd

# read the stock close price at D line
stockData = rd.ReadDataFromCSV("LZ_GPA_QUOTE_TCLOSE")

# takes pd.DataFream and return period as input
# out put the return over the input period
def CalcReturn(stockData,period = 1):
    # creating a empty pd DataFrame
    df = stockData.getDataFrame().ix[0::period]  # retrieve every period of rows
    return df/df.shift(1) - 1  # calc and return
# calc of the mean return of given stock
# takes the returns over certain period as a input
def CaclMeanReturn(stockReturns):
    return stockReturns.mean()

# sorting the mean returns
def sortMeanReturns(meanReturns):
    meanReturns.sort()






