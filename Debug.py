import pandas as pd
import numpy as np
import ReadDataFromCSV as rd

cap = rd.ReadFactorFromCSV("LZ_GPA_VAL_A_TCAP").Data
index = cap.index
columns = cap.columns

Factor = np.log(cap)

dateList = []
for i, item in enumerate(Factor.index):
    datelist = str(item.date()).split("-")
    datestr = datelist[0] + datelist[1] + datelist[2]
    dateList.append(datestr)
Factor.index = dateList

Factor.to_csv("LogTCap_1D.csv")
