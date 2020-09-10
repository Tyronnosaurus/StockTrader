import os
import sqlite3
from GetTickersListFromIndex import GetTickersListFromIndex
import yfinance as yf



#Given an index of companies, downloads to a database the share price history of each indexed company
def DownloadIndexHistoricData(index):
    ListOfTickers = GetTickersListFromIndex(index)   #Obtain a list of companies' tickers

    for ticker in ListOfTickers:
        DownloadStockHistoricData(ticker)


#Given a company's ticker (i.e. its trading symbol), downloads to a database the share price history
def DownloadStockHistoricData(ticker):
        data = yf.Ticker(ticker)
        #print(stock.info) #Caution: Causes error on some tickers: https://github.com/ranaroussi/yfinance/issues/208

        df = data.history(period="max")['Close']   #Download data. Only store the 'Close price' column
        #print(df)

        if (len(df)==0): return     #Ignore empty dataframe (possibly delisted company) 
        
        df.to_sql(ticker, conn, if_exists='replace', index=True)




Indexes = ['DAX', 'MDAX', 'IBEX 35']

#Connect to database (create if file doesn't exist)
workDir = os.getcwd()
conn = sqlite3.connect(workDir + '/FinancialData/StockDB.db')
c = conn.cursor()

for index in Indexes:
    DownloadIndexHistoricData(index)

conn.close()