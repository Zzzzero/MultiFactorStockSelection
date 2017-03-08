# -*- coding:utf-8 -*-
# import basic packages
import numpy as np
import pandas as pd
# import project file
import ReadDataFromCSV as rd
import Factor_test_frame_ports as ftp
# load stocks
stocks = rd.ReadStockFromCSV("LZ_GPA_QUOTE_TCLOSE")
industry = rd.ReadFactorFromCSV("LZ_GPA_INDU_ZX")
# load factor
pe = rd.ReadFactorFromCSV("LZ_GPA_VAL_PS_TTM")
# load stock index
stock_index = rd.IndexFromCSV("000001.SH")
# load trading capital
tradecap = rd.Read_Stock_Factor("LZ_GPA_VAL_A_TCAP")
# data prepare
# cacl stock returns on monthy ends #
# use to set test start time        #
start = "20150101"                  #
end = "20170301"                    #
stocks.setStartTime(start)          #
stocks.setEndTime(end)
industry.setStartTime(start)
industry.setEndTime(end)
pe.setStartTime(start)              #
pe.setEndTime(end)                  #
stock_index.setStartTime(start)     #
stock_index.setEndTime(end)         #
tradecap.setStartTime(start)        #
tradecap.setEndTime(end)            #
#####################################
#pe.dropNan()  # filter out poor data Factors
#peLabel = pe.getlabels()  # get current continent labels
# use same label as in Factor
#stocks.usePartially(peLabel)
#industry.usePartially(peLabel)
#tradecap.usePartially(peLabel)
# set rt time window
stocks.setValueAtMonthEnd()
industry.setValueAtMonthEnd()
tradecap.setValueAtMonthEnd()
pe.setValueAtMonthEnd()
stock_index.setValueAtMonthEnd()

# calc parameters
stock_indexrts = stock_index.cumRts()

test = ftp.Ports_test(5, pe, stocks, stock_index, tradecap, industry.Data, True)
test2 = ftp.Ports_test(5, pe, stocks, stock_index, tradecap)

test.showPlot()
test.factorRtCorr()
#test2.showPlot()
#test2.factorRtCorr()

