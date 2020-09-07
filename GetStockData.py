
import yfinance as yf


stock = yf.Ticker('BMW.DE')

print(stock.info) #Caution: Causes error on some tickers: https://github.com/ranaroussi/yfinance/issues/208