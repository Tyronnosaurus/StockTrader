import os
import sqlite3
from GetTickersListFromIndex import GetTickersListFromIndex
import yfinance as yf
from SqlHelpers import ListToSqlColumn


#Indexes to include. Yahoo Finances uses non-standard names for the indexes
Indexes = ['GDAXI',    #DAX
           'MDAXI',    #MDAX
           'IBEX']     #IBEX 35


#Given an index of companies, downloads to a database the share price history of the index and each individual company
def DownloadIndexHistoricData(index):
    ListOfTickers = GetTickersListFromIndex(index)   #Obtain a list of companies' tickers

    #Step 1: Create a list of the stocks in this index -> Table INDEXNAME_Stocks
    cur.execute("CREATE TABLE IF NOT EXISTS '%s' (Stocks varchar(20))" % (index + "_Stocks"))
    ListToSqlColumn(cur, '"' + index + '_Stocks"', ListOfTickers)

    #Step 2: Create a price history of the index -> Table INDEXNAME
    DownloadPriceHistory('^' + index)

    #Step 3: Create a price history of every stock  -> Tables STOCK1, STOCK2...
    for ticker in ListOfTickers:
        DownloadPriceHistory(ticker)



#Download price history of an index or stock
def DownloadPriceHistory(ticker):
        data = yf.Ticker(ticker)

        df = data.history(period="max")['Close']   #Download data. Only store the 'Close price' column

        if (len(df)==0): return()     #Ignore empty dataframe (possibly delisted company)

        ticker = ticker.replace('^','') #Yahoo Finance uses a '^' preffix in index names, but we don't want that for the name of tables or it will mess up SQL queries
        
        df.to_sql(ticker, conn, if_exists='replace', index=True)





#Connect to database (create if file doesn't exist)
workDir = os.getcwd()
conn = sqlite3.connect(workDir + '/FinancialData/StockDB.db')
cur = conn.cursor()

for index in Indexes:
    DownloadIndexHistoricData(index)

conn.close()