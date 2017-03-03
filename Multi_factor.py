# -*- coding:utf-8 -*-
# import basic packages
import numpy as np
import pandas as pd
# import project file
import ReadDataFromCSV as rd
import Factor_test_frame_ports as ftp
# load stocks
stocks = rd.ReadStockFromCSV("LZ_GPA_QUOTE_TCLOSE")
# load factor
pe = rd.ReadFactorFromCSV("LZ_GPA_VAL_PE")
# load stock index
stock_index = rd.IndexFromCSV()
# load trading capital
tradecap = rd.Read_Stock_Factor("LZ_GPA_VAL_A_TCAP")
# data prepare
# cacl stock returns on monthy ends #
# use to set test start time        #
start = "20140301"                  #
end = "20170301"                    #
stocks.setStartTime(start)          #
stocks.setEndTime(end)              #
pe.setStartTime(start)              #
pe.setEndTime(end)                  #
stock_index.setStartTime(start)     #
stock_index.setEndTime(end)         #
tradecap.setStartTime(start)        #
tradecap.setEndTime(end)            #
#####################################
pe.dropNan()  # filter out poor data Factors
peLabel = pe.getlabels()  # get current continent labels
# use same label as in Factor
stocks.usePartially(peLabel)
tradecap.usePartially(peLabel)
# set rt time window
stocks.setValueAtMonthEnd()
tradecap.setValueAtMonthEnd()
pe.setValueAtMonthEnd()
stock_index.setValueAtMonthEnd()

# calc parameters
rts, _ = stocks.calcReturn(stocks.Data)
indexrts, _ = stock_index.calcReturn(stock_index.Data)

test = ftp.Ports_test(5, pe, stocks, tradecap, False)
