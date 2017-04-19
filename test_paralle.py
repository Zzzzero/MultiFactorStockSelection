import pandas as pd
import numpy as np
import talib
from sklearn.decomposition import PCA
from joblib import delayed, Parallel
import multiprocessing

def a (x):
    return x**2

if __name__ == "__main__":
    A = Parallel(n_jobs=-1)(delayed(np.sqrt)(x) for x in range(1, 100))
    print(A)