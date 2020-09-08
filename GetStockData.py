from GetStockTickersInIndex import GetStockTickersInIndex
import sqlite3
import yfinance as yf


#Connect to database (create if file doesn't exist)
conn = sqlite3.connect('StockDB.db')
c = conn.cursor()

ListOfTickers = GetStockTickersInIndex('DAX')

for ticker in ListOfTickers:

    stock = yf.Ticker(ticker)
    #print(stock.info) #Caution: Causes error on some tickers: https://github.com/ranaroussi/yfinance/issues/208

    df = stock.history(period="max")['Close']   #Download data. Only store the 'Close price' column
    #print(df)

    df.to_sql(ticker, conn, if_exists='replace', index = True)

conn.close()