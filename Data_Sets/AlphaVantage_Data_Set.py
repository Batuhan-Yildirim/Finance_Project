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


class AlphaVantage:            # AlphaVantage documentation (https://www.alphavantage.co/documentation/)
    
    """Exception raised for errors in the input API Key.

    Attributes:
        Api Key Request --  request which caused the error
        message -- 5 API requests per minute and 500 requests per day
        website -- https://www.alphavantage.co/support/#api-key
    """
    
    def __init__(self, ticker):
        self.ticker = ticker
        configure()
    
 
    def CompanyInfo(self):     
        
        try:
            Company_info_url = f'https://www.alphavantage.co/query?function=OVERVIEW&symbol={self.ticker}&apikey={os.getenv("Alphavantage_key")}'
            r_info = requests.get(Company_info_url)
            Company = r_info.json()

            company_df = pd.DataFrame(Company.keys())
            company_df.rename(columns={0:"Title"},inplace= True)

            words = company_df["Title"]

            words_list = []

            for i in range(0,len(words)):
                list_words = words[i]

                pattern = "[A-Z][^A-Z]*"

                pattern_words = re.findall(pattern, list_words)
                pattern_words_new = " ".join(pattern_words).title()
                words_list.append(pattern_words_new)

            company_df["Title"] = words_list
            company_df.rename(columns={"index":"Title"}, inplace= True)


            values = pd.DataFrame(Company.values())
            company_df["Values"] = values
            
            try:
                return company_df
            except ConnectionError:
                error = "Connection Error!"
                return error
        
        except KeyError:
            print("This Symbol (Ticker) is not working! -- *Please Check or Try Another Symbol Such as, ['AAPL','C'] ")
        except TypeError:
            print("This Symbol (Ticker) is not working! -- *Please Check or Try Another Symbol Such as, ['AAPL','C'] ")      
        except ValueError:
            print("You should wait a minute! or you are exceed 5 API requests per minute and 500 requests per day!")

    def FinancialStatements(self):
        try:    
            FS = ["INCOME_STATEMENT","BALANCE_SHEET","CASH_FLOW"]   # Financial Statements

            FS_data = []
            IS = {}                                                 # Income Statements
            BS = {}                                                 # Balance Sheet
            CF = {}                                                 # Cash Flow


            for i in FS:
                FS_url = f'https://www.alphavantage.co/query?function={i}&symbol={self.ticker}&apikey={os.getenv("Alphavantage_key")}'
                FS_r = requests.get(FS_url)
                FS_data.append(FS_r.json())

                FS_data_df = pd.DataFrame(FS_data)
                
                df = {}
                for i in np.arange(0, len(FS_data_df)):
                    df[i] = FS_data_df.iloc[i].get("annualReports")

            IS = pd.DataFrame(df[0]).T.reset_index()
            BS = pd.DataFrame(df[1]).T.reset_index()
            CF = pd.DataFrame(df[2]).T.reset_index()

            FS = [IS,BS,CF]
            
            IS_fiscal_Date = IS.iloc[0].to_list()
            IS_index = IS.iloc[1].to_list()

            FS_pattern = []

            for i in np.arange(0, len(FS)):
                FS[i].replace("None",0,inplace = True)
                FS[i].fillna(0)

                FS[i].copy
                FS[i].loc[2:,[0,1,2,3,4]] = FS[i].loc[2:,[0,1,2,3,4]].astype("float64")
                
                FS[i].loc[:1] = IS_fiscal_Date 
                FS[i].loc[1] = IS_index
                
                FS_pattern.append(FS[i]["index"])


            one = FS_pattern[0]
            two = FS_pattern[1]
            three = FS_pattern[2]

            pattern = '[A-Z][^A-Z]*|[A-Z]*[^A-Z][^A-Z]*|[A-Z]*[^A-Z][^A-Z][^A-Z]*|[A-Z]*[^A-Z][^A-Z][^A-Z][^A-Z]*'

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
                FS[i].columns = IS_fiscal_Date
                FS[i] = FS[i].drop(0)

                FS[i].index.name = index_names[i]
            
            try:
                return FS
            except ConnectionError:
                error = "Connection Error!"
                return error
        
        except KeyError:
            print("This Symbol (Ticker) is not working! -- *Please Check or Try Another Symbol Such as, ['AAPL','C'] ")    
        except TypeError:
            print("This Symbol (Ticker) is not working! -- *Please Check or Try Another Symbol Such as, ['AAPL','C'] ")
        except ValueError:
            print("You should wait a minute! or you are exceed 5 API requests per minute and 500 requests per day!")

    def News(self):
        
        try:
            Company_news_url = f'https://www.alphavantage.co/query?function=NEWS_SENTIMENT&tickers={self.ticker}&apikey={os.getenv("Alphavantage_key")}'
            Company_news = requests.get(Company_news_url)
            Company_news_data = Company_news.json()

            news = pd.DataFrame(Company_news_data.get("feed"))

            news = news[["title","url"]]
            news.columns = ["News","News_Url"] 

            try:
                return news
            except ConnectionError:
                error = "Connection Error!"
                return error
        
        except KeyError:
            print("This Symbol (Ticker) is not working! -- *Please Check or Try Another Symbol Such as, ['AAPL','C'] ")
        except TypeError:
            print("This Symbol (Ticker) is not working! -- *Please Check or Try Another Symbol Such as, ['AAPL','C'] ")
        except ValueError:
            print("You should wait a minute! or you are exceed 5 API requests per minute and 500 requests per day!")
