<h1 align="center" id="title">Finance Machine Learning Project</h1>

In this Python project I developed a machine learning application for time series forecasting using my own custom dataset. To accomplish this I created a Python file to gather and organize the necessary data. Leveraging the neuralforecast library I trained a neural network model on the dataset to capture complex patterns and dependencies in the time series data. 
The project involved loading and preprocessing the dataset configuring the neural network model architecture and training the model using the neuralforecast library. I ensured the proper formatting of the data and handled any missing values or categorical variables. 

With the trained model I could generate accurate predictions for future time points based on historical data. The neuralforecast library provided the necessary functionalities for forecasting enabling me to leverage the power of neural networks in capturing intricate patterns. 

Throughout the project I paid careful attention to evaluating the performance of the machine learning application. Using appropriate evaluation metrics such as mean squared error (MSE), root mean squared error (RMSE), or mean absolute error (MAE), I assessed the accuracy and reliability of the predictions.

Overall this project demonstrated the effective use of a custom dataset Python programming and the neuralforecast library to develop a powerful machine learning application for time series forecasting. By leveraging neural networks I could unlock valuable insights and make accurate predictions in my specific problem domain.

---
# Dataset instruction 🗄

Each Dataset has unique keywords for getting data. So, this part is including instructions for that. !!

**❗️❗️**  **All Dataset Use a Symbol(Ticker). Such as AAPL(Apple Inc.) or TSLA(Tesla Co.)** **❗️❗️❗️**

## 🟣 Yfinance
* [Yfinance Woorkbook](https://github.com/Ybatuhan-EcoBooster/Finance_Library_Project/blob/main/Finance_Data_Sets/Yahoo_Finance_Data_Set.ipynb)

**Keywords**
> MajorHolder, MutualFundHolders, News, StockPrices, CompanyInfo, RealTimePrice

```RUN COMMAND
TSLA = DataSets.YahooFinance("TSLA","StockPrices")  # "StokPrices" is a keyword, TSLA is a Symbol(Ticker)
```
**Extra**
```RUN COMMAND
Ford_data_startdate = DataSets.YahooFinance("TSLA","StockPrices",start_date = "2010-06-29")  # "StokPrices" is a keyword, TSLA is a Symbol(Ticker)

Ford_data_enddate = DataSets.YahooFinance("TSLA","StockPrices",end_date  = "2010-06-29")

Ford_data_betweendate = DataSets.YahooFinance("TSLA","StockPrices",start_date = "2010-06-29",end_date  = "2011-06-29")

# OR

Ford_data_enddate = DataSets.YahooFinance("TSLA","StockPrices",period = "min")
```
        
            period = ['min','max','1w','1mo',1y']
            start_date = Start time is when the date starts your demand   --- Such as '2023-01-01'
            end_date   = 'End time is when the date End your demand   --- Such as '2023-01-01'
       
## 🔵 AlphaVantage API
* [AlphaVantage Woorkbook](https://github.com/Ybatuhan-EcoBooster/Finance_Library_Project/blob/main/Finance_Data_Sets/AlphaVantage_Data_Set.ipynb)

**Keywords**
> CompanyInfo, FinancialStatements, News

 ```RUN COMMAND
TSLA = DataSets.Alphavantage("AAPL","FinancialStatements")  # "StokPrices" is a keyword, TSLA is a Symbol(Ticker)
```
**🔖For Error**

```Exception raised for errors in the input API Key.

        Attributes:
            Api Key Request --  request which caused the error
            message -- 5 API requests per minute and 500 requests per day
            website -- https://www.alphavantage.co/support/#api-key
```

## ⚫️ FinancialModeling API
* [FinancialModelingprep Woorkbook](https://github.com/Ybatuhan-EcoBooster/Finance_Library_Project/blob/main/Finance_Data_Sets/Financial_Modeling_Prep.ipynb)

**Keywords**
> FinancialStatements, NASDAQ, DOWJONES, CompanyInfo, HistoricalPrice, FMPArticles, MarketCap, NYSEHours, DelistedCompanies, Ticker, HistoricalDividends,
> IPOCalander, EarningCalander, FinancialRatio, KeyMetrics, EntrpriseValue, DCFHistorical, CompanyRating, CompanyRatingHistorical

```RUN COMMAND
TSLA = DataSets.FinancialModelPrep("AAPL","FinancialStatements")  # "StokPrices" is a keyword, TSLA is a Symbol(Ticker)
```

**🔖For Error**

```Exception raised for errors in the input API Key.

        Attributes:
            Api Key Request --  request which caused the error
            message -- 250 requests per day
```

---

# Jupyter Notebooks Workbooks 🗂

## Datasets
* [Cryptocurrency Woorkbook](https://github.com/Ybatuhan-EcoBooster/Finance_Library_Project/blob/main/Finance_Data_Sets/Cryptocurrency_Data_Sets.ipynb)
* [Webscraper Woorkbook](https://github.com/Ybatuhan-EcoBooster/Finance_Library_Project/blob/main/Finance_Data_Sets/Web_Scraper.ipynb)

## Financial Formulas:
* [Financial Formulas Workbook](https://github.com/Ybatuhan-EcoBooster/Finance_Library_Project/blob/main/Financial_Formulas/Financial_formulas.ipynb)

## Graph:
* [Matplotlib Woorkbok](https://github.com/Ybatuhan-EcoBooster/Finance_Library_Project/blob/main/Graphs/Matplotlib_Graphs.ipynb)
* [Plotly Woorkbook](https://github.com/Ybatuhan-EcoBooster/Finance_Library_Project/blob/main/Graphs/Plotly_Graphs.ipynb)

## Machine Learning:
* [LSTM Neural Network Workbook](https://github.com/Ybatuhan-EcoBooster/Finance_Library_Project/blob/main/ML%20_Application/LSTM_Neural.ipynb)

---

## 📌 Sources 
- [AlphaVantage API](https://www.alphavantage.co/)
- [Financial Modeling Prep API](https://site.financialmodelingprep.com/developer/docs/financial-statements-list-api/)
- [Yfinance](https://pypi.org/project/yfinance/)
- [Tiingo API](https://www.tiingo.com/)
- [Yahoo Finance](https://finance.yahoo.com/)
- [CNN Money](https://edition.cnn.com/markets)
- [Investing.Com](https://www.investing.com/)
- [TradingView](https://tr.tradingview.com/)
- [LSTM Model](https://nixtla.github.io/neuralforecast/models.lstm.html)

---
# Notes:

**❗❗️When you downloaded this repository, You have to change the OS file path ❗️❗️❗️**
---
# For My Work Plan Template 📑

[💲Finance Data Analyst For Python Planner](https://pixelpallette.gumroad.com/l/FinanceDataAnalystPlanner?layout=profile)
---
# Soon 🔜

- More ML application
- More Financial Formulas
- Tiingo API 

