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
            def web_content_div(web_content, class_path):
                web_content_div = web_content.find_all("div", {"class": class_path})
                try:
                    spans = web_content_div[0].find_all("span")
                    fin = web_content_div[0].find("fin-streamer").get_text()
                    texts = [span.get_text() for span in spans]
                    texts.append(fin)
                    
                    ticker = web_content.find_all("h1",{"class":"D(ib) Fz(18px)"})
                    company_name = ticker[0].get_text()

                    texts.append(company_name)

                except IndexError:
                    texts = []

                return texts

            url = "https://finance.yahoo.com/quote/" + self.ticker + "?p=" + self.ticker + "&.tsrc=fin-srch"
            try:
                r = requests.get(url)
                web_content = BeautifulSoup(r.text, "lxml")
                texts = web_content_div(web_content, "D(ib) Mend(20px)")
                if texts != []:
                    output = f"Company Name: {texts[4]}" + ", "
                    output += f"Price: {texts[3]}" + ", "
                    output += f"Price change: {texts[1]}" + ", "
                    output += f"Price Change Percantage: {texts[0]}" + ", "
                else:
                    output = []

            except ConnectionError:
                output = []

            return output
        
        except KeyError:
            print("This Symbol (Ticker) is not working! -- *Please Check or Try Another Symbol Such as, ['AAPL','C'] ")
        except TypeError:
            print("This Symbol (Ticker) is not working! -- *Please Check or Try Another Symbol Such as, ['AAPL','C'] ")
        except ValueError:
            print("This Function Is Not Available!")