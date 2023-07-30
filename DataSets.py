# Error Message
import time

#Data Sets:
from Data_Sets.AlphaVantage_Data_Set import *
from Data_Sets.YahooFinance import *
from Data_Sets.FinancialModelPrep import *

# Warning Signs
import warnings
warnings.filterwarnings('ignore')


try:
    def rate_limiter(max_requests, interval):
        """
        Decorator function to enforce rate limiting on a function.

        Args:
            max_requests (int): Maximum number of requests allowed within the interval.
            interval (int): Time interval in seconds.

        Returns:
            function: Decorated function.
        """
        def decorator(func):
            request_times = []

            def wrapper(*args, **kwargs):
                # Check the number of requests made within the interval
                current_time = time.time()
                request_times.append(current_time)

                # Remove old requests outside the interval
                request_times[:] = [t for t in request_times if t > current_time - interval]

                # If the number of requests exceeds the limit, raise an exception
                if len(request_times) > max_requests:
                    raise Exception("Rate limit exceeded")

                # Call the original function
                return func(*args, **kwargs)

            return wrapper

        return decorator
    
    @rate_limiter(max_requests=5, interval=60)

    def Alphavantage(symbol, method_name):
        
        """Exception raised for errors in the input API Key.

        Attributes:
            Api Key Request --  request which caused the error
            message -- 5 API requests per minute and 500 requests per day
            website -- https://www.alphavantage.co/support/#api-key
        """
        
        methods = list(AlphaVantage.__dict__.keys())
        methods = methods[3:-1]

        alpha_vantage = AlphaVantage(symbol)

        if method_name in methods:
            
            alpha_method = method_name
            result = getattr(alpha_vantage, alpha_method)()
            return result
    
        else:

            return f"Invalid method name -- try: {methods}"

    
    def YahooFinance(symbol, method_name,period=None, start_date=None, end_date=None):
            
        """ Yahoo!, Y!Finance, and Yahoo! finance are registered trademarks of Yahoo, Inc. 

            Attributes:
            Website -- https://pypi.org/project/yfinance/ 
        """
        methods = list(Yahoo_Finance.__dict__.keys())
        methods = methods[3:-2]
            
        Yahoofinance = Yahoo_Finance(symbol)
        YahooFinance_2 = Yahoo_Finance(symbol).StockPrices(period,start_date,end_date)

        if method_name in methods:
                    
            Yahoofinance_method = method_name
            result = getattr(Yahoofinance, Yahoofinance_method)()

            if method_name != "StockPrices":
                return result
            else:
                return YahooFinance_2

        else:   
            return f"Invalid method name -- try: {methods}"
    

    @rate_limiter(max_requests=250, interval=60*60*24)

    def FinancialModelPrep(symbol,method_name):

        """Exception raised for errors in the input API Key.

        Attributes:
            Api Key Request --  request which caused the error
            message -- 250 requests per day
            website -- https://site.financialmodelingprep.com/developer/docs/
        """

        methods = list(FinanceModelPrep.__dict__.keys())
        methods = methods[2:-3]
        
        Finance_Model_Prep = FinanceModelPrep(symbol)

        if method_name in methods:

            finance_model_prep_method = method_name
            
            result = getattr(Finance_Model_Prep,finance_model_prep_method)()

            return result

        else:
            
            return f"Invalid method name -- try: {methods}"
 
except TypeError:
    
    print("Run commend ('ticker','information name') -- Such as Alphavantage('AAPL','News')")

except KeyError:
    
    print("Run commend ('ticker','information name') -- Such as Alphavantage('AAPL','News')")
