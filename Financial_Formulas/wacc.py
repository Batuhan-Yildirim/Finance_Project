# Core Libraries 
import pandas as pd
import numpy as np

# Datetime
from datetime import datetime

# For Data
import sys
sys.path.insert(0,"D:\dosyalar\Github\Finance_Project")
import DataSets

def wacc(self): # Weighted Average Cost of Capital (WACC)
    
    try:
        company = DataSets.Alphavantage(self,"FinancialStatements")
        Company_Last_Stock_Price = DataSets.YahooFinance(self,"StockPrices","min")
    
    except TypeError:
        print("This Symbol (Ticker) is not working! -- *Please Check or Try Another Symbol Such as, ['AAPL','C'] ")
    except KeyError:
        print("This Symbol (Ticker) is not working! -- *Please Check or Try Another Symbol Such as, ['AAPL','C'] ")

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

    beta_coff = covariance / variance
    beta_coff

    Cost_of_Equity = pd.DataFrame()
    Cost_of_Equity["Beta"] = [beta_coff]
    Cost_of_Equity["Market_return"] = [0.09]
    Cost_of_Equity["Risk_Free_Rate"] = [(DataSets.YahooFinance("^TNX","StockPrices","10y").iloc[-1]["Close"])/100]
    Cost_of_Equity["Cost_of_Equity"] = (Cost_of_Equity["Risk_Free_Rate"]) + (Cost_of_Equity["Beta"])*(Cost_of_Equity["Market_return"] - Cost_of_Equity["Risk_Free_Rate"])

    # Weight of Debt and Equity
        
    D_E = pd.DataFrame()
        
    D_E["Total"] = [Total_Debt + Market_Capitalazation]
    D_E["W_Total Debt"] = [Total_Debt / D_E.iloc[0]["Total"]]
    D_E["W_MarketCap"]  = [Market_Capitalazation / D_E.iloc[0]["Total"]]

    WACC = ((Cost_of_debt.iloc[0]["Cost_debt"]*D_E.iloc[0]["W_Total Debt"]*Cost_of_debt.iloc[0]["Cost_of_debt_after_tax"]) + (Cost_of_Equity.iloc[0]["Cost_of_Equity"]*D_E.iloc[0]["W_MarketCap"]))*100
        
    result = f"Weighted average cost of capital: {WACC}"
        
    return result
