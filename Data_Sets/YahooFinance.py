# Core Libraries 
import pandas as pd
import numpy as np

# For Yahoo Data Set
import yfinance as yf

# For Pattern
import re

#For website link requests
import requests
from requests.exceptions import ConnectionError
from bs4 import BeautifulSoup



class Yahoo_Finance:

    """ Yahoo!, Y!Finance, and Yahoo! finance are registered trademarks of Yahoo, Inc. 

        Attributes:
        Website -- https://pypi.org/project/yfinance/ 
    """
    
    def __init__(self, ticker):
        self.ticker = ticker
        self.Company_ticker = yf.Ticker(ticker)
    
    def MajorHolder(self):
        
        majorholder = self.Company_ticker.major_holders
        
        try:
            return majorholder
        
        except KeyError:
            print("This Symbol (Ticker) is not working! -- *Please Check or Try Another Symbol Such as, ['AAPL','C'] ")
        except TypeError:
            print("This Symbol (Ticker) is not working! -- *Please Check or Try Another Symbol Such as, ['AAPL','C'] ")
        except ValueError:
            print("This Function Is Not Available!")
 
    def MutualFundHolders(self):
        mutualfundholders = self.Company_ticker.mutualfund_holders
        
        try:
            return mutualfundholders 
        
        except KeyError:
            print("This Symbol (Ticker) is not working! -- *Please Check or Try Another Symbol Such as, ['AAPL','C'] ")
        except TypeError:
                print("This Symbol (Ticker) is not working! -- *Please Check or Try Another Symbol Such as, ['AAPL','C'] ")
        except ValueError:
            print("This Function Is Not Available!")

    def News(self):
        news = self.Company_ticker.news
        
        try:
            news = pd.DataFrame(news)
            news = news[["title", "publisher", "link"]]
            news.columns = ["Title", "Publisher", "News Link"]
            return news
        
        except KeyError:
            print("This Symbol (Ticker) is not working! -- *Please Check or Try Another Symbol Such as, ['AAPL','C'] ")
        except TypeError:
                print("This Symbol (Ticker) is not working! -- *Please Check or Try Another Symbol Such as, ['AAPL','C'] ")
        except ValueError:
            print("This Function Is Not Available!")

    def StockPrices(self, period=None, start_date=None, end_date=None):
        """ 
            period = ['min','max','1w','1mo',1y']
            start_date = Start time is when the date starts your demand   --- Such as '2023-01-01'
            end_date   = 'End time is when the date End your demand   --- Such as '2023-01-01'
        
        """

        try:
            if period is not None:
                try:
                    Data = self.Company_ticker.history(period=period)

                except AttributeError:
                    print("Try these periods: ['min','max','1w','1mo',1y']")
                
                except TypeError:
                     print("Please!! -- Try these periods: ['min','max','1w','1mo',1y']")
            
            elif start_date is not None:
                Data = yf.download(self.ticker, start=start_date)
            elif end_date is not None:
                Data = yf.download(self.ticker, end=end_date)
            elif start_date and end_date is not None:
                Data = yf.download(self.ticker, start=start_date, end=end_date)
            else:
                Data = yf.download(self.ticker, period="max")
            return Data
        
        except KeyError:
            print("This Symbol (Ticker) is not working! -- *Please Check or Try Another Symbol Such as, ['AAPL','C'] ")
        except ValueError:
            print("This Symbol (Ticker) is not available! -- *Please Try Another Symbol Such as, ['AAPL','C'] ")

    def CompanyInfo(self):
        try:
            info_keys = self.Company_ticker.info.keys()
            info = []
            for i in info_keys:
                get_info = self.Company_ticker.info.get(i)
                info.append(get_info)
            info = pd.DataFrame(info, index=info_keys, columns=["Information"])
            info.index.name = "Title"
            return info
               
        except KeyError:
            print("This Symbol (Ticker) is not working! -- *Please Check or Try Another Symbol Such as, ['AAPL','C'] ")
        except TypeError:
                print("This Symbol (Ticker) is not working! -- *Please Check or Try Another Symbol Such as, ['AAPL','C'] ")
        except ValueError:
            print("This Function Is Not Available!")

    def RealTimePrice(self):
        try:
            web_url = "https://money.cnn.com/quote/quote.html?utm_source=quote_search&symb=" + self.ticker
            web_request = requests.get(web_url)

            content = BeautifulSoup(web_request.text, "lxml")

            Data = content.find("td", {"class":"wsod_change"})
            Data = Data.find_all("span")
            
            Price_Change = Data[2].get_text()
            Price_Change_Per = Data[-1].get_text()
            

            RealTimePrice = [Price_Change,Price_Change_Per]
        
        except IndexError:
            RealTimePrice = []
        
        return RealTimePrice
        

