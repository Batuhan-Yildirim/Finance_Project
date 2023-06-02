# Core Libraries 
import pandas as pd
import numpy as np

# Datetime
from datetime import datetime

# Data Sets
import sys
sys.path.insert(0,"D:\dosyalar\Github\Finance_Project\Finance_Data_Sets")

import Data_Sets


class Formulas:

    def Bankruptcymodels(self):

        company = Data_Sets.AlphaVantage(self).Financial_Statements()

        total_current_asset = company[1][company[1]["fiscalDateEnding"] == "Total Current Assets"].values[0][1:]
        total_current_liabilities = company[1][company[1]["fiscalDateEnding"] == "Total Current Liabilities"].values[0][1:]

        company_working_capital = total_current_asset - total_current_liabilities

        total_asset = company[1][company[1]["fiscalDateEnding"] == "Total Assets"].values[0][1:]
        total_liabilities = company[1][company[1]["fiscalDateEnding"] == "Total Liabilities"].values[0][1:]
        
        Last_Stock_Price  = Data_Sets.Yahoo_Finance(self).get_data()
        
        Last_weekday = []
        for i in np.arange(0,5):
                current_date = datetime.now().date()
                one_year_ago = current_date - pd.DateOffset(years=i)
                business_days = pd.bdate_range(end=one_year_ago, periods=7)
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
    
    def WACC(self):
        
        company = Data_Sets.AlphaVantage(self).Financial_Statements()
        Company_Last_Stock_Price = Data_Sets.Yahoo_Finance(self).get_data(period="min")

        Outstanding_share        = company[1][company[1]["fiscalDateEnding"] == "Common Stock Shares Outstanding"].values[0][1]
        Market_Capitalazation    = Outstanding_share * Company_Last_Stock_Price["Close"].values[0]

        # Cost of Debt
        Total_Debt = company[1][company[1]["fiscalDateEnding"] == "Current Debt"].values[0][1] + company[1][company[1]["fiscalDateEnding"] == "Long Term Debt Noncurrent"].values[0][1] 

        Cost_of_debt = pd.DataFrame()
        Cost_of_debt["Interest_expense"] = [company[0][company[0]["fiscalDateEnding"] == "Interest Expense"].values[0][1]]
        Cost_of_debt["Total Debt"] = [Total_Debt]
        Cost_of_debt["Cost_debt"] = [company[0][company[0]["fiscalDateEnding"] == "Interest Expense"].values[0][1] / Total_Debt]
        Cost_of_debt["Income_tax_expense"] = [company[0][company[0]["fiscalDateEnding"] == "Income Tax Expense"].values[0][1]]
        Cost_of_debt["Before_Income_tax"] = [company[0][company[0]["fiscalDateEnding"] == "Income Before Tax"].values[0][1]] 
        Cost_of_debt["Effective_tax_rate"]= Cost_of_debt.iloc[0]["Income_tax_expense"] / Cost_of_debt.iloc[0]["Before_Income_tax"]
        Cost_of_debt["Cost_of_debt_after_tax"] = Cost_of_debt.iloc[0]["Cost_debt"] * (1 - Cost_of_debt.iloc[0]["Effective_tax_rate"])

        # Cost of Equity

        SP_500 = SPY = Data_Sets.Yahoo_Finance("SPY").get_data()
        SP_500 = SPY[SPY.index >= "2021-01-01"]
        SP_500 = SP_500["Close"]

        Company_data  = Data_Sets.Yahoo_Finance(self).get_data()
        Company_stock_price  = Company_data[Company_data.index >= "2021-01-01"]
        Company_stock_price  = Company_stock_price["Close"]

        SP_500_returns = SP_500.pct_change()
        Company_returns  = Company_stock_price.pct_change()

        covariance = Company_returns.cov(SP_500_returns) 
        variance = SP_500_returns.var()

        beta_coff = covariance / variance
        beta_coff

        Cost_of_Equity = pd.DataFrame()
        Cost_of_Equity["Beta"] = [beta_coff]
        Cost_of_Equity["Market_return"] = [0.09]
        Cost_of_Equity["Risk_Free_Rate"] = [(Data_Sets.Yahoo_Finance("^TNX").get_data(period="10y").iloc[-1]["Close"]) / 100]
        Cost_of_Equity["Cost_of_Equity"] = (Cost_of_Equity["Risk_Free_Rate"]) + (Cost_of_Equity["Beta"])*(Cost_of_Equity["Market_return"] - Cost_of_Equity["Risk_Free_Rate"])

        # Weight of Debt and Equity
        
        D_E = pd.DataFrame()
        
        D_E["Total"] = [Total_Debt + Market_Capitalazation]
        D_E["W_Total Debt"] = [Total_Debt / D_E.iloc[0]["Total"]]
        D_E["W_MarketCap"]  = [Market_Capitalazation / D_E.iloc[0]["Total"]]

        WACC = ((Cost_of_debt.iloc[0]["Cost_debt"]*D_E.iloc[0]["W_Total Debt"]*Cost_of_debt.iloc[0]["Cost_of_debt_after_tax"]) + (Cost_of_Equity.iloc[0]["Cost_of_Equity"]*D_E.iloc[0]["W_MarketCap"]))*100
        
        result = f"Weighted average cost of capital: {WACC}"
        
        return result
    
    def Beta(self):

        SP_500 = SPY = Data_Sets.Yahoo_Finance("SPY").get_data()
        SP_500 = SPY[SPY.index >= "2021-01-01"]
        SP_500 = SP_500["Close"]

        Company_data  = Data_Sets.Yahoo_Finance(self).get_data()
        Company_stock_price  = Company_data[Company_data.index >= "2021-01-01"]
        Company_stock_price  = Company_stock_price["Close"]

        SP_500_returns = SP_500.pct_change()
        Company_returns  = Company_stock_price.pct_change()

        covariance = Company_returns.cov(SP_500_returns) 
        variance = SP_500_returns.var()

        beta = covariance / variance

        beta = f"Beta Coefficient of {self}: {beta}"

        return beta


t = "GS"
print(Formulas.Bankruptcymodels(t))
