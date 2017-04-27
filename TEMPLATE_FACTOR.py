import pandas as pd
import numpy as np
import ReadDataFromCSV as rd
"""read data"""


'''compute signal'''
Factor = pd.DataFrame(index=price.index, columns=price.columns)

"""store the Factor in correct index"""
dateList = []
for i, item in enumerate(Factor.index):
    datelist = str(item.date()).split("-")
    datestr = datelist[0] + datelist[1] + datelist[2]
    dateList.append(datestr)

Factor.index = dateList

Factor.to_csv("name.csv")
