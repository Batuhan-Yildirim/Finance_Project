# Core Libraries 
import pandas as pd
import numpy as np
import requests

#for API Key
from dotenv import load_dotenv
import os
def configure():
    load_dotenv()


class tiingo(): # Tiingo documentation (https://www.tiingo.com/documentation/general/overview)

    """Exception raised for errors in the input API Key.

    Attributes:
        Api Key Request --  request which caused the error
        Unique Symbols per Month -- 500 (Free Verison)
        Max Requests Per Hour -- 50 (Free Version)
        Max Requests Per Day -- 1000(Free Version)
        message -- 50 API requests per hour and 1000 requests per day
        website -- https://www.tiingo.com/about/pricing
    """
    def __init__(self, ticker=None):
        self.ticker = ticker
        configure()

    def Ticker():
        Stickers = pd.read_csv("D:\dosyalar\Github\Finance_Project\Finance_Data_Sets\TickerForTiingo\supported_tickers.csv")
        
        return Stickers

    def StockPrices(self,startdate = None,enddate = None,Resamplefreq = None):
        try:
            headers = {'Content-Type': 'application/json'}

            requestResponse = requests.get(f'https://api.tiingo.com/tiingo/daily/{self.ticker}?token={os.getenv("Tiingo_key")}', headers=headers)
            meta_data = requestResponse.json()

            first_date = meta_data.get("startDate")

            if startdate is not None:
                requestResponse = requests.get(f'https://api.tiingo.com/tiingo/daily/{self.ticker}/prices?startDate={startdate}&token={os.getenv("Tiingo_key")}', 
                                        headers=headers)
                data_price = requestResponse.json()
            elif enddate is not None:
                requestResponse = requests.get(f'https://api.tiingo.com/tiingo/daily/{self.ticker}/prices?endDate={enddate}&token={os.getenv("Tiingo_key")}', 
                                        headers=headers)
                data_price = requestResponse.json()
            elif startdate and enddate is not None:
                requestResponse = requests.get(f'https://api.tiingo.com/tiingo/daily/{self.ticker}/prices?startDate={startdate}&endDate={enddate}&token={os.getenv("Tiingo_key")}', 
                                        headers=headers)
                data_price = requestResponse.json()
            elif Resamplefreq is not None:
                requestResponse = requests.get(f'https://api.tiingo.com/tiingo/daily/{self.ticker}/prices?startDate={startdate}&endDate={enddate}&resampleFreq={Resamplefreq}&token={os.getenv("Tiingo_key")}', 
                                        headers=headers)
                data_price = requestResponse.json()
            else:
                requestResponse = requests.get(f'https://api.tiingo.com/tiingo/daily/{self.ticker}/prices?startDate={first_date}&token={os.getenv("Tiingo_key")}', 
                                            headers=headers)
                data_price = requestResponse.json()
            
            Stock = pd.DataFrame(data_price)
            Stock["date"] = pd.to_datetime(Stock["date"])
            
            return Stock
        
        except KeyError:
            print("Data is gathering !!")
        except TypeError:
            print("Data is gathering !!")      
        except ValueError:
            print("You should wait hour or day !! -- 50 API requests per hour and 1000 requests per day or This Date is not acceptable")

        
    def CompanyInfo(self):
        try:
            headers = {'Content-Type': 'application/json'}

            requestResponse = requests.get(f'https://api.tiingo.com/tiingo/daily/{self.ticker}?token={os.getenv("Tiingo_key")}', headers=headers)
            meta_data = requestResponse.json()

            meta_data_keys = list(meta_data.keys())

            meta_data_df = []
            for i in meta_data_keys:
                df = meta_data.get(i)
                meta_data_df.append(df)
            meta_data_df = pd.DataFrame(meta_data_df)
            meta_data_df.rename(columns={0:"Value"}, inplace=True)
            
            return meta_data_df

        except KeyError:
            print("This Symbol (Ticker) is not working! -- *Please Check or Try Another Symbol Such as, ['AAPL','C']")
        except TypeError:
                print("This Symbol (Ticker) is not working! -- *Please Check or Try Another Symbol Such as, ['AAPL','C']")
        except ValueError:
            print("This Function Is Not Available!")

    def CryptoPrice(self,startdate = None,enddate = None,Resamplefreq = None):
        try:
            headers = {'Content-Type': 'application/json'}

            if startdate is not None:
                requestResponse = requests.get(f'https://api.tiingo.com/tiingo/crypto/prices?tickers={self.ticker}&startDate={startdate}&resampleFreq=1day&token={os.getenv("Tiingo_key")}', 
                                        headers=headers)
                data_crypto = requestResponse.json()
            elif enddate is not None:
                requestResponse = requests.get(f'https://api.tiingo.com/tiingo/crypto/prices?tickers={self.ticker}&endDate={enddate}&resampleFreq=1day&token={os.getenv("Tiingo_key")}', 
                                        headers=headers)
                data_crypto = requestResponse.json()
            elif startdate and enddate is not None:
                requestResponse = requests.get(f'https://api.tiingo.com/tiingo/crypto/prices?tickers={self.ticker}&startDate={startdate}&endDate={enddate}&resampleFreq=1day&token={os.getenv("Tiingo_key")}', 
                                        headers=headers)
                data_crypto = requestResponse.json()
            elif Resamplefreq is not None:
                requestResponse = requests.get(f'https://api.tiingo.com/tiingo/crypto/prices?tickers={self.ticker}&startDate={startdate}&endDate={enddate}&resampleFreq={Resamplefreq}&token={os.getenv("Tiingo_key")}', 
                                        headers=headers)
                data_crypto = requestResponse.json()
            else:
                requestResponse = requests.get(f'https://api.tiingo.com/tiingo/crypto/prices?tickers={self.ticker}&startDate=2020-01-01&resampleFreq=1day&token={os.getenv("Tiingo_key")}', 
                                            headers=headers)
                data_crypto = requestResponse.json()
            
            crypto = pd.DataFrame(data_crypto)
            crypto = pd.DataFrame( crypto["priceData"][0])
            crypto["date"] = pd.to_datetime(crypto["date"])
            
            return crypto
        
        except KeyError:
            print("Data is gathering !!")
        except TypeError:
            print("Data is gathering !!")      
        except ValueError:
            print("You should wait hour or day !! -- 50 API requests per hour and 1000 requests per day or This Date is not acceptable")
        
    def FOREX(self,startdate = None,enddate = None,Resamplefreq = None, daily = None):
        if daily != True:
            try:
                headers = {'Content-Type': 'application/json'}

                if startdate is not None:
                    requestResponse = requests.get(f'https://api.tiingo.com/tiingo/fx/{self.ticker}/prices?&startDate={startdate}&resampleFreq=1day&token={os.getenv("Tiingo_key")}', 
                                            headers=headers)
                    data_forex = requestResponse.json()
                elif enddate is not None:
                    requestResponse = requests.get(f'https://api.tiingo.com/tiingo/fx/{self.ticker}/prices?&endDate={enddate}&resampleFreq=1day&token={os.getenv("Tiingo_key")}', 
                                            headers=headers)
                    data_forex = requestResponse.json()
                elif startdate and enddate is not None:
                    requestResponse = requests.get(f'https://api.tiingo.com/tiingo/fx/{self.ticker}/prices?&startDate={startdate}&endDate={enddate}&resampleFreq=1day&token={os.getenv("Tiingo_key")}', 
                                            headers=headers)
                    data_forex = requestResponse.json()
                elif Resamplefreq is not None:
                    requestResponse = requests.get(f'https://api.tiingo.com/tiingo/fx/{self.ticker}/prices?&startDate={startdate}&endDate={enddate}&resampleFreq={Resamplefreq}&token={os.getenv("Tiingo_key")}', 
                                            headers=headers)
                    data_forex = requestResponse.json()
                
                else:
                    requestResponse = requests.get(f'https://api.tiingo.com/tiingo/fx/{self.ticker}/prices?&startDate=2020-01-01&resampleFreq=1day&token={os.getenv("Tiingo_key")}', 
                                                headers=headers)
                    data_forex = requestResponse.json()
                
                forex = pd.DataFrame(data_forex)
                forex["date"] = pd.to_datetime(forex["date"])

                
                return forex
    
            except KeyError:
                print("Data is gathering !!")
            except TypeError:
                print("Data is gathering !!")      
            except ValueError:
                print("You should wait hour or day !! -- 50 API requests per hour and 1000 requests per day or This Date is not acceptable")
        
        else:
            headers = {'Content-Type': 'application/json'}
            requestResponse = requests.get(f'https://api.tiingo.com/tiingo/fx/top?tickers={self.ticker}&token={os.getenv("Tiingo_key")}', headers=headers)
            data_forex_d = requestResponse.json()

            forex_d = pd.DataFrame(data_forex_d)
            return forex_d
        
    def IEX(self,startdate = None,enddate = None,Resamplefreq = None, daily = None):
        if daily != True:
            try:
                headers = {'Content-Type': 'application/json'}

                if startdate is not None:
                    requestResponse = requests.get(f'https://api.tiingo.com/iex/{self.ticker}/prices?startDate={startdate}&resampleFreq=1hour&columns=open,high,low,close,volume&token={os.getenv("Tiingo_key")}', 
                                                   headers=headers)
                    data_IEX = requestResponse.json()
                elif enddate is not None:
                    requestResponse = requests.get(f'https://api.tiingo.com/iex/{self.ticker}/prices?endDate={enddate}&resampleFreq=1hour&columns=open,high,low,close,volume&token={os.getenv("Tiingo_key")}', 
                                            headers=headers)
                    data_IEX = requestResponse.json()
                elif startdate and enddate is not None:
                    requestResponse = requests.get(f'https://api.tiingo.com/iex/{self.ticker}/prices?&startDate={startdate}&endDate={enddate}&resampleFreq=1hour&columns=open,high,low,close,volume&token={os.getenv("Tiingo_key")}', 
                                            headers=headers)
                    data_IEX = requestResponse.json()
                elif Resamplefreq is not None:
                    requestResponse = requests.get(f'https://api.tiingo.com/iex/{self.ticker}/prices?&startDate={startdate}&endDate={enddate}&resampleFreq={Resamplefreq}&columns=open,high,low,close,volume&token={os.getenv("Tiingo_key")}', 
                                            headers=headers)
                    data_IEX = requestResponse.json()
                
                else:
                    requestResponse = requests.get(f'https://api.tiingo.com/iex/{self.ticker}/prices?&startDate=2023-01-01&resampleFreq=1hour&columns=open,high,low,close,volume&token={os.getenv("Tiingo_key")}', 
                                                headers=headers)
                    data_IEX = requestResponse.json()
                
                IEX = pd.DataFrame(data_IEX)
                IEX["date"] = pd.to_datetime(IEX["date"])

                
                return IEX
    
            except KeyError:
                print("Data is gathering !!")
            except TypeError:
                print("Data is gathering !!")      
            except ValueError:
                print("You should wait hour or day !! -- 50 API requests per hour and 1000 requests per day or This Date is not acceptable")
        
        else:
            headers = {'Content-Type': 'application/json'}
            requestResponse = requests.get(f'https://api.tiingo.com/iex/?tickers={self.ticker},spy&token={os.getenv("Tiingo_key")}', headers=headers)
            data_IEX_d = requestResponse.json()

            IEX_d = pd.DataFrame(data_IEX_d)
            return IEX_d     
    
    def KeyMetrics(self):

        headers = {'Content-Type': 'application/json'}
        requestResponse = requests.get(f'https://api.tiingo.com/tiingo/fundamentals/{self.ticker}/daily?token={os.getenv("Tiingo_key")}', headers=headers)
        data_metrics = requestResponse.json()

        metrics = pd.DataFrame(data_metrics)
        metrics["date"] = pd.to_datetime(metrics["date"])

        return metrics
    
    def FSFormulas(self, Cashflow = None, BalanceSheet = None, IncomeStatement = None, Other = None,formuladescraption = None):
        if formuladescraption != True:
            headers = {'Content-Type': 'application/json'}
            requestResponse = requests.get(f'https://api.tiingo.com/tiingo/fundamentals/{self.ticker}/statements?token={os.getenv("Tiingo_key")}', headers=headers)
            data_multi = requestResponse.json()
            data_multi = pd.DataFrame(data_multi)

            multi_frame_keys = list(data_multi.iloc[0]["statementData"].keys())

            if Cashflow == True:
            
                FS_cashflow = []

                for i in np.arange(0,len(data_multi)):
                    cashflow = data_multi.iloc[i,3].get(multi_frame_keys[0])
                    FS_cashflow.append(cashflow)
                    FS_cashflow[i] = pd.DataFrame(FS_cashflow[i])
                    FS_cashflow[i].index.name = data_multi.iloc[i,0]
                    FS_cashflow[i].rename(columns={"dataCode":multi_frame_keys[0],"value":"Value"}, inplace = True)


                return FS_cashflow
            
            elif IncomeStatement == True:
                
                FS_incomestatement= []

                for i in np.arange(0,len(data_multi)):
                    incomestatement = data_multi.iloc[i,3].get(multi_frame_keys[2])
                    FS_incomestatement.append(incomestatement)
                    FS_incomestatement[i] = pd.DataFrame(FS_incomestatement[i])
                    FS_incomestatement[i].index.name = data_multi.iloc[i,0]
                    FS_incomestatement[i].rename(columns={"dataCode":multi_frame_keys[2],"value":"Value"}, inplace = True)


                return FS_incomestatement
            
            elif BalanceSheet == True:
                
                FS_balancesheet = []

                for i in np.arange(0,len(data_multi)):
                    balancesheet = data_multi.iloc[i,3].get(multi_frame_keys[1])
                    FS_balancesheet.append(balancesheet)
                    FS_balancesheet[i] = pd.DataFrame(FS_balancesheet[i])
                    FS_balancesheet[i].index.name = data_multi.iloc[i,0]
                    FS_balancesheet[i].rename(columns={"dataCode":multi_frame_keys[1],"value":"Value"}, inplace = True)

                return FS_balancesheet
            
            elif Other == True:
                FS_overview = []

                for i in np.arange(0,len(data_multi)):
                    overview = data_multi.iloc[i,3].get(multi_frame_keys[3])
                    FS_overview.append(overview)
                    FS_overview[i] = pd.DataFrame(FS_overview[i])
                    FS_overview[i].index.name = data_multi.iloc[i,0]
                    FS_overview[i].rename(columns={"dataCode":multi_frame_keys[3],"value":"Value"}, inplace = True)

                return FS_overview
            
            else:
                FS_cashflow = []
                FS_balancesheet = []
                FS_incomestatement = []
                FS_overview = []

                for i in np.arange(0,len(data_multi)):
                    
                    cashflow = data_multi.iloc[i,3].get(multi_frame_keys[0])
                    FS_cashflow.append(cashflow)
                    FS_cashflow[i] = pd.DataFrame(FS_cashflow[i])
                    FS_cashflow[i].index.name = data_multi.iloc[i,0]
                    FS_cashflow[i].rename(columns={"dataCode":multi_frame_keys[0],"value":"Value"}, inplace = True)
                    
                    balancesheet = data_multi.iloc[i,3].get(multi_frame_keys[2])
                    FS_balancesheet.append(balancesheet)
                    FS_balancesheet[i] = pd.DataFrame(FS_balancesheet[i])
                    FS_balancesheet[i].index.name = data_multi.iloc[i,0]
                    FS_balancesheet[i].rename(columns={"dataCode":multi_frame_keys[2],"value":"Value"}, inplace = True)
                    
                    incomestatement = data_multi.iloc[i,3].get(multi_frame_keys[1])
                    FS_incomestatement.append(incomestatement)
                    FS_incomestatement[i] = pd.DataFrame(FS_incomestatement[i])
                    FS_incomestatement[i].index.name = data_multi.iloc[i,0]
                    FS_incomestatement[i].rename(columns={"dataCode":multi_frame_keys[1],"value":"Value"}, inplace = True)

                    overview = data_multi.iloc[i,3].get(multi_frame_keys[3])
                    FS_overview.append(overview)
                    FS_overview[i] = pd.DataFrame(FS_overview[i])
                    FS_overview[i].index.name = data_multi.iloc[i,0]
                    FS_overview[i].rename(columns={"dataCode":multi_frame_keys[3],"value":"Value"}, inplace = True)

                return FS_balancesheet,FS_cashflow,FS_incomestatement,FS_overview
                            

        else:
            headers = {'Content-Type': 'application/json'}
            requestResponse = requests.get(f'https://api.tiingo.com/tiingo/fundamentals/definitions?token={os.getenv("Tiingo_key")}', headers=headers)
            data_Fdes = requestResponse.json()
            Fundamentals = pd.DataFrame(data_Fdes)
            return Fundamentals


