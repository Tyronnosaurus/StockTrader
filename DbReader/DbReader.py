import sqlite3
from datetime import timedelta
import os


#Fetches financial data stored in an SQL database (once it's downloaded, it's faster and safer to use a local database for simulations) 
class DbReader:
    
    def __init__(self):
        workDir = os.getcwd()
        self.conn = sqlite3.connect(workDir + '/DbReader/StockDB.db')
        self.cur = self.conn.cursor()


    def GetPrice(self, ticker, _datetime):
        found = False
        while (not found):
            self.cur.execute("SELECT Close FROM '%s' WHERE Date = '%s'" % (ticker, _datetime))
            price = self.cur.fetchall()
            if (len(price)): found = True
            else: _datetime = _datetime - timedelta(days=1)

        return(price[0][0]) #We just retrieved a number but it's inside a list of tuples, so we must present it as a single float

    
    def GetStocksInIndex(self, index):
        tableName = index + "_Stocks"
        result = self.cur.execute("SELECT * FROM '%s'" % (tableName))
        formattedResult = [i[0] for i in result]    #SELECT returns a list of lists (rows x columns). There's only 1 column, so we convert it to a simple list
        return(formattedResult)