import ReadDataFromCSV as rd
import pandas as pd

########## section to import raw data ############
price = rd.ReadStockFromCSV("LZ_GPA_QUOTE_TCLOSE")
####### set param here #########
sens = 1  # detecter sensitivity
window = 30  # time window
tor = 30  # torlerant for nan values
################################
rts = price.calcReturn()

factorUp = pd.DataFrame(columns=rts.columns)
factorDown = pd.DataFrame(columns=rts.columns)

for index in rts.index[window:]:
    print(index)
    # the index
    datelist = str(index.date()).split("-")
    datestr = datelist[0] + datelist[1] + datelist[2]

    currentData = rts.loc[:index].tail(window)
    std = currentData.std()
    mean = currentData.mean()
    uplim = mean+std*sens
    downlim = mean-std*sens
    ups = currentData > uplim
    downs = currentData < downlim

    factorUp.loc[datestr] = ups.sum().values.astype(float)/window
    factorDown.loc[datestr] = downs.sum().values.astype(float)/window

factor = factorUp - factorDown

factor.to_csv("30W1SensPPR.csv")
