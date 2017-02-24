# -*- coding:utf-8 -*-
#
# import basic packages
import numpy as np
import pandas as pd

class Stocks():
    stocks = pd.DataFrame()
    def __init__(self, FileName, path="D:/cStrategy/Factor/"):
        self.stocks = pd.read_csv(path+FileName+".csv")
    def get