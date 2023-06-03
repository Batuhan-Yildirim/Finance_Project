# Core Libraries 
import pandas as pd
import numpy as np

# Datetime
from datetime import datetime

# For Data
import sys
sys.path.insert(1,"D:\dosyalar\Github\Finance_Project\Data_Sets")

import DataSets


def beta(self):

    SP_500 = SPY = DataSets.YahooFinance("SPY","StockPrices")
    SP_500 = SPY[SPY.index >= "2021-01-01"]
    SP_500 = SP_500["Close"]

    try:
    
        Company_data  = DataSets.YahooFinance(self,"StockPrices")
    
    except TypeError:
        print("This Symbol (Ticker) is not working! -- *Please Check or Try Another Symbol Such as, ['AAPL','C'] ")
    except KeyError:
        print("This Symbol (Ticker) is not working! -- *Please Check or Try Another Symbol Such as, ['AAPL','C'] ")

    Company_stock_price  = Company_data[Company_data.index >= "2021-01-01"]
    Company_stock_price  = Company_stock_price["Close"]

    SP_500_returns = SP_500.pct_change()
    Company_returns  = Company_stock_price.pct_change()

    covariance = Company_returns.cov(SP_500_returns) 
    variance = SP_500_returns.var()

    beta_result = covariance / variance

    beta = f"Beta Coefficient of {self}: {beta_result}"

    return beta
