# Core Libraries 
import pandas as pd
import numpy as np

# Datetime
from datetime import datetime

# For Data
import sys
sys.path.insert(1,"D:\dosyalar\Github\Finance_Project\Data_Sets")

import DataSets


def Bankruptcymodels(self):

        try:
                company = DataSets.Alphavantage(self,"FinancialStatements")
        
        except TypeError:
                print("This Symbol (Ticker) is not working! -- *Please Check or Try Another Symbol Such as, ['AAPL','C'] ")
        except KeyError:
                print("This Symbol (Ticker) is not working! -- *Please Check or Try Another Symbol Such as, ['AAPL','C'] ")

        total_current_asset = company[1][company[1]["fiscalDateEnding"] == "Total Current Assets"].values[0][1:]
        total_current_liabilities = company[1][company[1]["fiscalDateEnding"] == "Total Current Liabilities"].values[0][1:]

        company_working_capital = total_current_asset - total_current_liabilities

        total_asset = company[1][company[1]["fiscalDateEnding"] == "Total Assets"].values[0][1:]
        total_liabilities = company[1][company[1]["fiscalDateEnding"] == "Total Liabilities"].values[0][1:]
        
        try:
                Last_Stock_Price  = DataSets.YahooFinance(self,"StockPrices")
        
        except TypeError:
                print("This Symbol (Ticker) is not working! -- *Please Check or Try Another Symbol Such as, ['AAPL','C'] ")
        except KeyError:
                print("This Symbol (Ticker) is not working! -- *Please Check or Try Another Symbol Such as, ['AAPL','C'] ")
        
        Last_weekday = []
        for i in np.arange(0,5):
                current_date = datetime.now().date()
                one_year_ago = current_date - pd.DateOffset(years=i)
                business_days = pd.date_range(end=one_year_ago, periods=7)
                last_friday = [business_days[business_days.weekday == 4].max()]

                Last_weekday.append(last_friday)
        Last_weekday = pd.DataFrame(Last_weekday)
        Last_weekday[0] = pd.DatetimeIndex(Last_weekday[0].dt.strftime("%Y-%m-%d"))
        
        values = []
        for i in np.arange(0,len(Last_weekday)):
                Data_prices = Last_Stock_Price["Close"][Last_Stock_Price.index == Last_weekday.iloc[i][0]]
                values.append(Data_prices)
        values = pd.DataFrame(values)
        
        df_without_nan = values.dropna(axis = 0, how= "all")
        LastStockPrice = df_without_nan.values.flatten()
        LastStockPrice = pd.DataFrame(LastStockPrice)
        LastStockPrice = LastStockPrice.dropna()
        LastStockPrice.index = Last_weekday[0]
        
        Market_value_of_equity = company[1][company[1]["fiscalDateEnding"] == "Common Stock Shares Outstanding"].values[0][1:] * LastStockPrice[0].values[:]

        
        Net_Interest_Income = company[0][company[0]["fiscalDateEnding"] == "Net Interest Income"].values[0][1:]  
        Non_Interest_Income = company[0][company[0]["fiscalDateEnding"] == "Non Interest Income"].values[0][1:]
        Revenue = Net_Interest_Income + Non_Interest_Income


        A = company_working_capital / total_asset
        B = company[1][company[1]["fiscalDateEnding"] == "Retained Earnings"].values[0][1:] / total_asset
        C = company[0][company[0]["fiscalDateEnding"] == "Ebit"].values[0][1:] / total_asset
        D = Market_value_of_equity / total_liabilities
        E = Revenue / total_asset

        Altman_z_score = (1.2*A) + (1.4*B) + (3.3*C) + (0.6*D) + (1.0*E)
        
        Scores = pd.DataFrame(Altman_z_score, index=company[1].columns[1:], columns=["Altman Z Score"])

        C_1 = company[0][company[0]["fiscalDateEnding"] == "Income Before Tax"].values[0][1:] / total_liabilities
        D_1 = Revenue / total_asset

        Springate_score = (1.03*A) + (3.07*C) + (0.66*C_1) + (0.4*D_1)

        Scores["| Springate Score"] = Springate_score

        A_1 = company[0][company[0]["fiscalDateEnding"] == "Net Income"].values[0][1:] / total_asset
        B_1 = total_liabilities / total_asset
        C_2 = total_current_asset / total_current_liabilities

        constant = [-4.336,-4.336,-4.336,-4.336,-4.336]

        Zmijewski_Score = (constant) + (-4.513*A_1) + (5.679*B_1) + (0.004 * C_2)

        Scores["| Zmijewski Score"] = Zmijewski_Score

        return Scores
