# -*- coding:utf-8 -*-
# import basic packages
import numpy as np
import pandas as pd
# import project file
import ReadDataFromCSV as rd
import Factor_test_frame_ports as ftp

# load stocks
stocks = rd.readStockFromCSV("LZ_GPA_QUOTE_TCLOSE")
# load factor
PE = rd.readFactorFromCSV("LZ_GPA_VAL_PE")
# load stock index
stock_index = rd.indexFromCSV()
# load trading capital
tradecap = rd.read_Stock_Factor("LZ_GPA_VAL_A_TCAP")

# data prepare

# cacl stock returns on monthy ends# use to set test start time#########
start = "20150101"                  #
end = "20170301"                    #
stocks.setStartTime(start)          #
stocks.setEndTime(end)              #
PE.setStartTime(start)              #
PE.setEndTime(end)                  #
stock_index.setStartTime(start)     #
stock_index.setEndTime(end)         #
tradecap.setStartTime(start)
tradecap.setEndTime(end)
#####################################
PE.dropNan()  # filter out poor data Factors
PeLabel = PE.getlabels()  # get current continent labels
# use same label as in Factor
stocks.usePartially(PeLabel)
tradecap.usePartially(PeLabel)
# set rt time window
stocks.setValueAtMonthEnd()
tradecap.setValueAtMonthEnd()
PE.setValueAtMonthEnd()
stock_index.setValueAtMonthEnd()

# calc parameters
rts, _ = stocks.CalcReturn(stocks.Data)
indexrts, _ = stock_index.CalcReturn(stock_index.Data)

test = ftp.ports_test(100, PE.Data, rts, tradecap.Data)




