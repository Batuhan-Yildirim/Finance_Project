# Core Libraries 
import pandas as pd
import numpy as np

# Datetime
from datetime import datetime

# Error Message
import time

#Formulas
from BankruptcyModels import *
from Beta import *
from wacc import *

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

def BankruptcyModels(self):
    """ 
        Springate Score = The Springate score is one of the well-known bankruptcy prediction models, 
        which is developed on the basis of the Altman model. In the process of developing a model of the 19 financial 
        ratios that were considered the best, Springate selected four coefficients, based on which the model was built.

        Zmijewski Score = The Zmijewski score is one of the most well-known models for predicting bankruptcy of enterprises, 
        based on metrics like performance, leverage, and financial liquidity.

        Altman's Z Score = The Altman Z-score is the output of a credit-strength 
        test that gauges a publicly traded manufacturing company's likelihood of bankruptcy.

    """
    BankruptcyModels = Bankruptcymodels(self)

    return BankruptcyModels

def Beta(self): # Beta Coefficient
    """
        The beta coefficient formula is a financial metric that measures, 
        how likely the price of a stock/security will change concerning the movement in the market price.
    
    """

    Beta_coefficent = beta(self)

    return Beta_coefficent

def WACC(self): # Weighted Average Cost of Capital (WACC)
    """
        A firm’s Weighted Average Cost of Capital (WACC) represents its blended cost of capital across all sources, 
        including common shares, preferred shares, and debt.
    """

    WACC = wacc(self)

    return WACC
