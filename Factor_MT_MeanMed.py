import pandas as pd
import numpy as np
import ReadDataFromCSV as rd

def binaryDet(series):
    states = [False, True]
    same1 = 0
    same2 = 0
    transit1 = 0
    transit2 = 0
    '''handling NaN'''
    numNa = series.isnull().sum()
    numOfObser = len(series)
    if numNa == numOfObser:
        return np.nan
    if numNa > (numOfObser/2):
        return np.nan
    series = series.dropna()

    for i, state in enumerate(series):
        if i == 0:
            continue
            # omit the first state
        if series.iloc[i-1] == states[0]:
            if state == states[0]:
                same1 += 1
            else:
                transit1 += 1
        if series.iloc[i-1] == states[1]:
            if state == states[1]:
                same2 += 1
            else:
                transit2 += 1

    if same1 + transit1 == 0:
        return 1  # the case all state are True, perfect pos momentum, 1 as perfect momentum
    else:
        p = float(same1) / float(same1 + transit1)
    if same2 + transit2 == 0:
        return 1  # the case all state are False, perfect neg momentum, 1 as perfect momentum
    else:
        q = float(same2) / float(same2 + transit2)
    return p*q-(1-p)*(1-q)
data = rd.ReadStockFromCSV("LZ_GPA_QUOTE_TCLOSE")
adj = rd.ReadDataFromCSV("LZ_GPA_CMFTR_CUM_FACTOR")
price = data.Data*adj.Data
daliyRt = price / price.shift(1) - 1
binaryProfit = daliyRt > 0
binaryLose = daliyRt < 0
binaryState = pd.DataFrame(index=binaryLose.index, columns=binaryLose.columns)

for i, col in enumerate(binaryLose):
    binaryState[col].loc[binaryProfit[col] == True] = binaryProfit[col].loc[binaryProfit[col] == True]
    binaryState[col].loc[binaryLose[col] == True] = ~binaryLose[col].loc[binaryLose[col] == True]
'''this method should adjusted for NaN value to be robust on all stocks'''
mt20df = pd.DataFrame(index=binaryState.index, columns=binaryState.columns)
mt10df = pd.DataFrame(index=binaryState.index, columns=binaryState.columns)
for i, item in enumerate(binaryState.index):
    if i < 20:
        continue
    df20 = binaryState.tail(20)
    df10 = binaryState.tail(10)

    mt20 = df20.apply(lambda x: binaryDet(x))
    mt10 = df10.apply(lambda x: binaryDet(x))

    mt20df.loc[item] = mt20
    mt10df.loc[item] = mt10


