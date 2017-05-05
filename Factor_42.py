import pandas as pd
import numpy as np
import ReadDataFromCSV as rd

'''name: alpha_42'''

"""read data"""
vwap = rd.ReadFactorFromCSV("LZ_GPA_QUOTE_AVGPRICE").Data
close = rd.ReadFactorFromCSV("LZ_GPA_QUOTE_TCLOSE").Data
index = close.index
columns = close.columns
'''compute signal'''
Factor = pd.DataFrame(index=index, columns=columns)

minus = vwap - close
plus = vwap + close

minus_rank = minus.rank(axis=1)
plus_rank = plus.rank(axis=1)

Factor = minus_rank / plus_rank

"""store the Factor in correct index"""
dateList = []
for i, item in enumerate(Factor.index):
    datelist = str(item.date()).split("-")
    datestr = datelist[0] + datelist[1] + datelist[2]
    dateList.append(datestr)
Factor.index = dateList
Factor.to_csv("intradayAL42_1D.csv")