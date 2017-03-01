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

rts = stocks.CalcReturn(21)
rtDate = stocks.getRtPeriodStart(21)
factorAtRtDate = PE.prepareFactorAtDate(rtDate)
normValue = PE.standarlizedFactors(factorAtRtDate)

