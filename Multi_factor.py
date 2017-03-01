# -*- coding:utf-8 -*-
# import basic packages
import numpy as np
import pandas as pd
# import project file
import ReadDataFromCSV as rd

# load stocks
stocks = rd.readStockFromCSV("LZ_GPA_QUOTE_TCLOSE")
# load factor
PE = rd.readFactorFromCSV("LZ_GPA_VAL_PE")
# load stock index
stock_index = rd.indexFromCSV()

# data prepare
PE.dropNan()  # filter out poor data Factors
PeLabel = PE.getlabels()  # get current continent labels
stocks.usePartially(PeLabel)  # use stock which contains in PE
stocks.setValueAtMonthEnd()
PE.setValueAtMonthEnd()
stock_index.setValueAtMonthEnd()

# cacl stock returns on monthy ends
rts, _ = stocks.CalcReturn(stocks.Data)
indexrts, _ = stock_index.CalcReturn(stock_index.Data)

rtPremium = rd.rtOverIndex(rts, indexrts)  # excess return of stocks over given index


# starardlized value of factors
normValue = PE.standarlizedFactors(PE.Data)  # standardized Factor values


