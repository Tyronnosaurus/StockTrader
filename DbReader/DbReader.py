import sqlite3
from datetime import timedelta, datetime
import os


#Fetches financial data stored in an SQL database (once it's downloaded, it's faster and safer to use a local database for simulations) 
class DbReader:
    
    def __init__(self):
        workDir = os.getcwd()
        self.conn = sqlite3.connect(workDir + '/DbReader/StockDB.db')
        self.cur = self.conn.cursor()

    #Get Close price for a particular day (or the most recent day if markets are closed)
    def GetPrice(self, ticker, _datetime):
        found = False
        while (not found):
            self.cur.execute("SELECT Close FROM '%s' WHERE Date = '%s'" % (ticker, _datetime))
            price = self.cur.fetchall()
            if (len(price)): found = True
            else: _datetime = _datetime - timedelta(days=1)

        return(price[0][0]) #We just retrieved a number but it's inside a list of tuples, so we must present it as a single float

    
    #Returns list of stocks (tickers) in an index
    def GetStocksInIndex(self, index):
        tableName = index + "_Stocks"
        result = self.cur.execute("SELECT * FROM '%s'" % (tableName))
        formattedResult = [i[0] for i in result]    #SELECT returns a list of lists (rows x columns). There's only 1 column, so we convert it to a simple list
        return(formattedResult)


    #Returns prices for N days
    def GetPricesFromPeriod(self, ticker, endTime, totalDays):
        self.cur.execute("SELECT * FROM '%s' WHERE Date<='%s' ORDER BY Date DESC LIMIT '%s'" % (ticker, endTime, totalDays))
        prices = self.cur.fetchall()
        prices = [i[1] for i in prices] #We've got a list of lists, so we convert it to a simple list
        return(prices)


    #
    def _getLastDayRelativePosition(self, ticker, lastDay, totalDays):
        pricesList = self.GetPricesFromPeriod(ticker, lastDay, totalDays)   #Get prices from last N days
        indexLastDay = totalDays - 1
        posLastDay = self._getIndexInSortedArray(pricesList, indexLastDay)  #Get position of last day if the list was sorted
        return(posLastDay / totalDays)  #Return as a percentage
    

    #Returns position of a list item if the list was sorted
    def _getIndexInSortedArray(self, arr, idx):
        #To optimize, rather than sorting we just count how many smaller items there are
        count = 0
        for i,_ in enumerate(arr):
            if (arr[i] < arr[idx]):  #If element is smaller then increase the smaller count
                count += 1
    
            if (arr[i] == arr[idx] and i < idx):  #If element is equal then also increase count (only if it occurs before)
                count += 1
        return(count)


    def IsLow(self, ticker, lastDay, totalDays, maxPercentage):
        return(self._getLastDayRelativePosition(ticker, lastDay, totalDays) <= maxPercentage)


