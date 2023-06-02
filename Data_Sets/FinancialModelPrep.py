# Core Libraries 
import pandas as pd
import numpy as np
import requests

# For Pattern
import re

#for API Key
from dotenv import load_dotenv
import os

def configure():
    load_dotenv()


class FinanceModelPrep:            #for Api Key --- Financial Modeling Prep Api Key  
                                   # (https://site.financialmodelingprep.com/developer/docs/#Financial-Statements-List)
    def __init__(self, ticker=None):
        self.ticker = ticker
        configure()
    
    """Exception raised for errors in the input API Key.

    Attributes:
        Api Key Request --  request which caused the error
        message -- 250 requests per day
        website -- https://site.financialmodelingprep.com/developer/docs/
    """

    def FinancialStatements(self):
        
        try:
            FS_list = ["income-statement","balance-sheet-statement","cash-flow-statement"] # Financial Statement
            data = []
            
            for i in FS_list:
                urlx = f"https://financialmodelingprep.com/api/v3/{i}/{self.ticker}?limit=240&apikey={os.getenv('FinancialMP_key')}"
                r_infox = requests.get(urlx)
                fsx = r_infox.json()
                data.append(fsx)

            IS = pd.DataFrame(data[0]).T.reset_index()          # Income Statement
            FS_columns = IS.iloc[0].to_list()
            BS = pd.DataFrame(data[1]).T.reset_index()          # Balance Sheet Statement
            CF = pd.DataFrame(data[2]).T.reset_index()          # Cash Flow Statement

            pattern = '[A-Z][^A-Z]*|[A-Z]*[^A-Z][^A-Z]*|[A-Z]*[^A-Z][^A-Z][^A-Z]*|[A-Z]*[^A-Z][^A-Z][^A-Z][^A-Z]*'

            FS = [IS,BS,CF]


            one = FS[0]["index"]
            two = FS[1]["index"]
            three = FS[2]["index"]

            FS_0_join = []
            for i in np.arange(0, len(one)):
                FS_0_pattern = one[i]
                FS_0_findall = re.findall(pattern,FS_0_pattern)
                FS_0_join.append(" ".join(FS_0_findall).title())
            FS[0]["index"] = FS_0_join

            FS_1_join = []
            for z in np.arange(0, len(two)):
                FS_1_pattern = two[z]
                FS_1_findall = re.findall(pattern,FS_1_pattern)
                FS_1_join.append(" ".join(FS_1_findall).title())
            FS[1]["index"] = FS_1_join

            FS_2_join = []
            for q in np.arange(0, len(three)):
                FS_2_pattern = three[q]
                FS_2_findall = re.findall(pattern,FS_2_pattern)
                FS_2_join.append(" ".join(FS_2_findall).title())
            FS[2]["index"] = FS_2_join

            index_names = ["INCOME STATEMENT","BALANCE SHEET","CASH FLOW"]


            for i in np.arange(0,3):
                FS[i].columns = FS_columns
                FS[i] = FS[i].drop(0)

                FS[i].rename_axis(None, axis=1, inplace=True)

                FS[i].index.name = index_names[i]

                FS[i].rename(columns={"date":"Date"}, inplace=True)

                FS[i] = FS[i].iloc[:-1]
            
            return FS
        
        except KeyError:
            print("This API work Only THE U.S. Companies --- You can try another Ticker ['AAPL',' C', 'MSFT']")
        except TypeError:
            print("This API work Only THE U.S. Companies --- You can try another Ticker ['AAPL',' C', 'MSFT']")
        except ValueError:
            print("You exceed 250 requests per day!") 
    
    def NASDAQ(self):
        # run commend -- FinanceModelPrep("")
        try:
            NASDAQ_100_url = f"https://financialmodelingprep.com/api/v3/nasdaq_constituent?apikey={os.getenv('FinancialMP_key')}"
            NASDAQ_100_r   = requests.get(NASDAQ_100_url)
            NASDAQ_100_data = NASDAQ_100_r.json()
            NASDAQ_100_df = pd.DataFrame(NASDAQ_100_data)
            NASDAQ_100_df.columns = ["Symbol","Name","Sector","Sub Sector","Head Quarter","Date First Added","CIK","Founded"]
            return NASDAQ_100_df
        
        except KeyError:
            print("You can use like this! ---- FinancialModelPrep('','NASDAQ')")
        except TypeError:
            print("You can use like this! ---- FinancialModelPrep('','NASDAQ')")
        except ValueError:
            print("You exceed 250 requests per day!")
        
    def DOWJONES(self):
        # run commend -- FinanceModelPrep("")

        try:
            Dow_Jones_url = f"https://financialmodelingprep.com/api/v3/historical/dowjones_constituent?apikey={os.getenv('FinancialMP_key')}"
            Dow_Jones_r   = requests.get(Dow_Jones_url)
            Dow_Jones_data = Dow_Jones_r.json()
            Dow_Jones_df = pd.DataFrame(Dow_Jones_data)
            Dow_Jones_df.columns = ["Date Add","Added Security","Removed Ticker","Removed Security","Date","Symbol","Reason"]

            return Dow_Jones_df
        
        except KeyError:
            print("You can use like this! ---- FinancialModelPrep('','DOWJONES')")
        except TypeError:
            print("You can use like this! ---- FinancialModelPrep('','DOWJONES')")
        except ValueError:
            print("You exceed 250 requests per day!")
    
    def CompanyInfo(self):
        try:
            Company_profile_url = f"https://financialmodelingprep.com/api/v3/profile/{self.ticker}?apikey={os.getenv('FinancialMP_key')}"
            Company_profile_r   = requests.get(Company_profile_url)
            Company_profile     = Company_profile_r.json()

            Company_df = pd.DataFrame(Company_profile).T
            Company_df = Company_df.reset_index()
            
            pattern = '[A-Z][^A-Z]*|[A-Z]*[^A-Z][^A-Z]*|[A-Z]*[^A-Z][^A-Z][^A-Z]*|[A-Z]*[^A-Z][^A-Z][^A-Z][^A-Z]*'
            index = Company_df["index"]
            index_list = []

            for i in np.arange(0, len(index)):
                index_pattern = index[i]
                index_findall = re.findall(pattern,index_pattern)
                index_list.append(" ".join(index_findall).title())

            Company_df["index"] = index_list
            Company_df.columns =["Description Title","Description"]

            return Company_df
        
        except KeyError:
            print("This API work Only THE U.S. Companies --- You can try another Ticker ['AAPL',' C', 'MSFT']")
        except TypeError:
            print("This API work Only THE U.S. Companies --- You can try another Ticker ['AAPL',' C', 'MSFT']")
        except ValueError:
            print("You exceed 250 requests per day!")
    
    def HistoricalPrice(self):
        
        try:
            Stock_daily_url = f"https://financialmodelingprep.com/api/v3/historical-price-full/{self.ticker}?apikey={os.getenv('FinancialMP_key')}"
            Stock_daily_r = requests.get(Stock_daily_url)
            Stock_daily_data = Stock_daily_r.json()

            Stock_daily = pd.DataFrame(Stock_daily_data.get("historical"))
            
            Companydf = FinanceModelPrep(self.ticker).CompanyInfo()
            
            name = Companydf[Companydf["Description Title"] == "Company Name"].values[0][1]

            Stock_daily.index.name = name

            return Stock_daily
        
        except KeyError:
            print("This API work Only THE U.S. Companies --- You can try another Ticker ['AAPL',' C', 'MSFT']")
        except TypeError:
            print("This API work Only THE U.S. Companies --- You can try another Ticker ['AAPL',' C', 'MSFT']")
        except ValueError:
            print("You exceed 250 requests per day!")

    def FMPArticles (self):
        # run commend -- FinanceModelPrep("")

        try:
            FMP_Article_url = f"https://financialmodelingprep.com/api/v3/fmp/articles?page=0&size=20&apikey={os.getenv('FinancialMP_key')}"
            FMP_Article_r = requests.get(FMP_Article_url)
            FMP_Article_data = FMP_Article_r.json()
            
            content = pd.DataFrame(FMP_Article_data.get("content"))
            content = content[["title","date","tickers","link","author","site"]]
            
            return content
        
        except KeyError:
            print("You can use like this! ---- FinancialModelPrep('','FMPArticles')")
        except TypeError:
            print("You can use like this! ---- FinancialModelPrep('','FMPArticles')")
        except ValueError:
            print("You exceed 250 requests per day!")
    

    def MarketCap(self):
        try:
        
            Historical_market_cap_url = f"https://financialmodelingprep.com/api/v3/historical-market-capitalization/{self.ticker}?limit=100&apikey={os.getenv('FinancialMP_key')}"
            Historical_market_cap_r   = requests.get(Historical_market_cap_url)
            Historical_market_cap     = Historical_market_cap_r.json()

            Historical_market_cap_df = pd.DataFrame(Historical_market_cap)

            return Historical_market_cap_df
        
        except KeyError:
            print("This API work Only THE U.S. Companies --- You can try another Ticker ['AAPL',' C', 'MSFT']")
        except TypeError:
            print("This API work Only THE U.S. Companies --- You can try another Ticker ['AAPL',' C', 'MSFT']")
        except ValueError:
            print("You exceed 250 requests per day!")

    def NYSEHours(self):
        # run commend -- FinanceModelPrep("")

        try:
            NYSE_trading_hourse_url = f"https://financialmodelingprep.com/api/v3/is-the-market-open?apikey={os.getenv('FinancialMP_key')}"
            NYSE_trading_hourse_r   = requests.get(NYSE_trading_hourse_url)
            NYSE_trading_hourse     = NYSE_trading_hourse_r.json()
            
            name = NYSE_trading_hourse.get('stockExchangeName')
            
            stockMarketHours = NYSE_trading_hourse.get('stockMarketHours')

            print(f"NYSE Opening Hourse = {stockMarketHours.get('openingHour')} -- NYSE Close Hourse {stockMarketHours.get('closingHour')}")
            
            stockMarketHolidays = pd.DataFrame(NYSE_trading_hourse.get('stockMarketHolidays'))
            stockMarketHolidays.index.name = name
            
            return stockMarketHolidays
        
        except KeyError:
            print("You can use like this! ---- FinancialModelPrep('','NYSEHours')")
        except TypeError:
            print("You can use like this! ---- FinancialModelPrep('','NYSEHours')")
        except ValueError:
            print("You exceed 250 requests per day!")
    
    def DelistedCompanies(self):
        # run commend -- FinanceModelPrep("")

        try:
        
            Delisted_companies_url = f"https://financialmodelingprep.com/api/v3/delisted-companies?page=0&apikey={os.getenv('FinancialMP_key')}"
            Delisted_companies_r   = requests.get(Delisted_companies_url)
            Delisted_companies     = Delisted_companies_r.json()
            Delisted_companies     = pd.DataFrame(Delisted_companies)
            Delisted_companies.columns = ["Symbol","Company Name","Exchange","IPO Date","Delisted Date"]
            
            return Delisted_companies
        
        except KeyError:
            print("You can use like this! ---- FinancialModelPrep('','DelistedCompanies')")
        except TypeError:
            print("You can use like this! ---- FinancialModelPrep('','DelistedCompanies')")
        except ValueError:
            print("You exceed 250 requests per day!")
        
    def Ticker(self):
        
        try:
            Exchange = ["ETF","MUTUAL_FUND ","COMMODITY","INDEX","CRYPTO","FOREX","TSX","AMEX","NASDAQ","NYSE","EURONEXT"]
            print(Exchange)
            
            Exchange_input = input("Enter Exchange Markets: ")

            ticker_search_url = f"https://financialmodelingprep.com/api/v3/search?query=AA&limit=50&exchange={Exchange_input}&apikey={os.getenv('FinancialMP_key')}"
            ticker_search_r   = requests.get(ticker_search_url)
            ticker_search     = ticker_search_r.json()
            ticker_search_df   = pd.DataFrame(ticker_search)
            ticker_search_df.columns = ["Symbol","Name","Currency","Stock Exchange","Exchange Short Name"]

            return ticker_search_df
        
        except KeyError:
            print("You can use like this! ---- FinancialModelPrep('','Ticker')")
        except TypeError:
            print("You can use like this! ---- FinancialModelPrep('','Ticker')")
        except ValueError:
            print("You exceed 250 requests per day!")
    
    def HistoricalDividends(self):
        
        try:
            Historical_dividends_url = f"https://financialmodelingprep.com/api/v3/historical-price-full/stock_dividend/{self.ticker}?apikey={os.getenv('FinancialMP_key')}"
            Historical_dividends_r   = requests.get(Historical_dividends_url)
            Historical_dividends     = Historical_dividends_r.json()
            
            symbol = pd.DataFrame(Historical_dividends)

            Historical_dividends = pd.DataFrame(Historical_dividends.get("historical"))
            
            Historical_dividends["Symbol"] = symbol["symbol"]

            historical_reverse = Historical_dividends.columns.to_list()

            Historical_dividends = Historical_dividends[historical_reverse[::-1]]

            return Historical_dividends
        
        except KeyError:
            print("This API work Only THE U.S. Companies --- You can try another Ticker ['AAPL',' C', 'MSFT']")
        except TypeError:
            print("This API work Only THE U.S. Companies --- You can try another Ticker ['AAPL',' C', 'MSFT']")
        except ValueError:
            print("You exceed 250 requests per day!")
    
    def IPOCalander(self):
        # run commend -- FinanceModelPrep("")
        
        try:
            IPO_Calander_url = f"https://financialmodelingprep.com/api/v3/ipo_calendar?from=2020-09-01&to=2020-11-01&apikey={os.getenv('FinancialMP_key')}"
            IPO_Calander_r   = requests.get(IPO_Calander_url)
            IPO_Calander     = IPO_Calander_r.json()

            IPO_Calander = pd.DataFrame(IPO_Calander)
            IPO_Calander.columns = ["Date","Company","Symbol","Exchange","Actions","Shares","Price Range","Market Cap"]
            return IPO_Calander
        
        except KeyError:
            print("You can use like this! ---- FinancialModelPrep('','IPOCalander')")
        except TypeError:
            print("You can use like this! ---- FinancialModelPrep('','IPOCalander')")
        except ValueError:
            print("You exceed 250 requests per day!")    
    
    def EarningCalander(self):
        # run commend -- FinanceModelPrep("")

        try:
            Earning_Calander_url = f"https://financialmodelingprep.com/api/v3/earning_calendar?apikey={os.getenv('FinancialMP_key')}"
            Earning_Calander_r   = requests.get(Earning_Calander_url)
            Earning_Calander     = Earning_Calander_r.json()
            
            Earning_Calander = pd.DataFrame(Earning_Calander)
            Earning_Calander = Earning_Calander[["date","symbol","time","revenueEstimated","fiscalDateEnding","updatedFromDate"]]
            Earning_Calander.columns = ["Date","Symbol","Time","Revenue Estimated","Fiscal Date Ending","Update From Date"]
            
            return Earning_Calander
        
        except KeyError:
            print("You can use like this! ---- FinancialModelPrep('','EarningCalander')")
        except TypeError:
            print("You can use like this! ---- FinancialModelPrep('','EarningCalander')")
        except ValueError:
            print("You exceed 250 requests per day!") 


    def FinancialRatio(self):

        try:  
            Financial_Ratio_url = f"https://financialmodelingprep.com/api/v3/ratios-ttm/{self.ticker}?apikey={os.getenv('FinancialMP_key')}"
            Financial_Ratio_r   = requests.get(Financial_Ratio_url)
            Financial_Ratio    = Financial_Ratio_r.json()
            Financial_Ratio_df = pd.DataFrame(Financial_Ratio).T.reset_index()

            pattern = '[A-Z][^A-Z]*|[A-Z]*[^A-Z][^A-Z]*|[A-Z]*[^A-Z][^A-Z][^A-Z]*|[A-Z]*[^A-Z][^A-Z][^A-Z][^A-Z]*'

            index = Financial_Ratio_df["index"]

            index_list = []

            for i in np.arange(0, len(index)):
                
                index_pattern = index[i]
                index_findall = re.findall(pattern,index_pattern)
                index_list.append(" ".join(index_findall).title())

            Financial_Ratio_df["index"] = index_list

            Financial_Ratio_df.columns =["Description Title","Description"]

            return Financial_Ratio_df
        
        except KeyError:
            print("This API work Only THE U.S. Companies --- You can try another Ticker ['AAPL',' C', 'MSFT']")
        except TypeError:
            print("This API work Only THE U.S. Companies --- You can try another Ticker ['AAPL',' C', 'MSFT']")
        except ValueError:
            print("You exceed 250 requests per day!")

    def KeyMetrics(self):
        
        try:
            Key_metrics_url = f"https://financialmodelingprep.com/api/v3/key-metrics-ttm/{self.ticker}?limit=40&apikey={os.getenv('FinancialMP_key')}"
            Key_metrics_r   = requests.get(Key_metrics_url)
            Key_metrics   = Key_metrics_r.json()
            
            Key_metrics = pd.DataFrame(Key_metrics).T.reset_index()
            pattern = '[A-Z][^A-Z]*|[A-Z]*[^A-Z][^A-Z]*|[A-Z]*[^A-Z][^A-Z][^A-Z]*|[A-Z]*[^A-Z][^A-Z][^A-Z][^A-Z]*'

            index = Key_metrics["index"]

            index_list = []

            for i in np.arange(0, len(index)):
            
                index_pattern = index[i]
                index_findall = re.findall(pattern,index_pattern)
                index_list.append(" ".join(index_findall).title())

            Key_metrics["index"] = index_list

            Key_metrics.columns =["Description Title","Description"]

            return Key_metrics
        
        except KeyError:
            print("This API work Only THE U.S. Companies --- You can try another Ticker ['AAPL',' C', 'MSFT']")
        except TypeError:
            print("This API work Only THE U.S. Companies --- You can try another Ticker ['AAPL',' C', 'MSFT']")
        except ValueError:
            print("You exceed 250 requests per day!")
    
    def EntrpriseValue(self):
        
        try:
            Enterprise_value_url = f"https://financialmodelingprep.com/api/v3/enterprise-values/{self.ticker}?limit=40&apikey={os.getenv('FinancialMP_key')}"
            Enterprise_value_r   = requests.get(Enterprise_value_url)
            Enterprise_value   = Enterprise_value_r.json()

            Enterprise_value = pd.DataFrame(Enterprise_value)
            Enterprise_value.columns = ["Symbol","Date","Stock Price","Number Of Shares","Market Capitalization","Minus Cash And Cash Equivalents","Add Total Debt","Enterprise Value"]
            
            return Enterprise_value
        
        except KeyError:
            print("This API work Only THE U.S. Companies --- You can try another Ticker ['AAPL',' C', 'MSFT']")
        except TypeError:
            print("This API work Only THE U.S. Companies --- You can try another Ticker ['AAPL',' C', 'MSFT']")
        except ValueError:
            print("You exceed 250 requests per day!")
        
    def DCFHistorical(self):

        try:
            Current_dcf_url = f"https://financialmodelingprep.com/api/v3/discounted-cash-flow/{self.ticker}?apikey={os.getenv('FinancialMP_key')}"
            Current_dcf_r   = requests.get(Current_dcf_url)
            Current_dcf   = Current_dcf_r.json()

            print(Current_dcf)

            Historical_dcf_url = f"https://financialmodelingprep.com/api/v3/historical-discounted-cash-flow-statement/{self.ticker}?apikey={os.getenv('FinancialMP_key')}"
            Historical_dcf_r   = requests.get(Historical_dcf_url)
            Historical_dcf   = Historical_dcf_r.json()
            Historical_dcf = pd.DataFrame(Historical_dcf)

            return Historical_dcf
        except KeyError:
            print("This API work Only THE U.S. Companies --- You can try another Ticker ['AAPL',' C', 'MSFT']")
        except TypeError:
            print("This API work Only THE U.S. Companies --- You can try another Ticker ['AAPL',' C', 'MSFT']")
        except ValueError:
            print("You exceed 250 requests per day!")

    def CompanyRating(self):
        
        try:
            Company_rating_url = f"https://financialmodelingprep.com/api/v3/rating/{self.ticker}?apikey={os.getenv('FinancialMP_key')}"
            Company_rating_r   = requests.get(Company_rating_url)
            Company_rating   = Company_rating_r.json()
            Company_rating = pd.DataFrame(Company_rating).T.reset_index()

            pattern = '[A-Z][^A-Z]*|[A-Z]*[^A-Z][^A-Z]*|[A-Z]*[^A-Z][^A-Z][^A-Z]*|[A-Z]*[^A-Z][^A-Z][^A-Z][^A-Z]*'

            index = Company_rating["index"]

            index_list = []

            for i in np.arange(0, len(index)):
            
                index_pattern = index[i]
                index_findall = re.findall(pattern,index_pattern)
                index_list.append(" ".join(index_findall).title())

            Company_rating["index"] = index_list

            Company_rating.columns =["Description Title","Description"]

            return Company_rating
        
        except KeyError:
            print("This API work Only THE U.S. Companies --- You can try another Ticker ['AAPL',' C', 'MSFT']")
        except TypeError:
            print("This API work Only THE U.S. Companies --- You can try another Ticker ['AAPL',' C', 'MSFT']")
        except ValueError:
            print("You exceed 250 requests per day!")
    
    def CompanyRatingHistorical(self):
        try:
            Historical_Company_rating_url = f"https://financialmodelingprep.com/api/v3/historical-rating/{self.ticker}?limit=100&apikey={os.getenv('FinancialMP_key')}"
            Historical_Company_rating_r   = requests.get(Historical_Company_rating_url)
            Historical_Company_rating  = Historical_Company_rating_r.json()
            Historical_Company_rating = pd.DataFrame(Historical_Company_rating)
            pattern = '[A-Z][^A-Z]*|[A-Z]*[^A-Z][^A-Z]*|[A-Z]*[^A-Z][^A-Z][^A-Z]*|[A-Z]*[^A-Z][^A-Z][^A-Z][^A-Z]*'

            index = Historical_Company_rating.columns.to_list()

            index_list = []

            for i in np.arange(0, len(index)):
            
                index_pattern = index[i]
                index_findall = re.findall(pattern,index_pattern)
                index_list.append(" ".join(index_findall).title())

            Historical_Company_rating.columns = index_list

            return Historical_Company_rating
        
        except KeyError:
            print("This API work Only THE U.S. Companies --- You can try another Ticker ['AAPL',' C', 'MSFT']")
        except TypeError:
            print("This API work Only THE U.S. Companies --- You can try another Ticker ['AAPL',' C', 'MSFT']")
        except ValueError:
            print("You exceed 250 requests per day!")
