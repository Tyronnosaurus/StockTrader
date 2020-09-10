import sqlite3
from datetime import timedelta
import os


class DataReader:
    
    def __init__(self):
        workDir = os.getcwd()
        self.conn = sqlite3.connect(workDir + '/FinancialData/StockDB.db')
        self.cur = self.conn.cursor()


    def GetPrice(self, ticker, _datetime):
        found = False
        while (not found):
            self.cur.execute("SELECT Close FROM '%s' WHERE Date = '%s'" % (ticker, _datetime))
            price = self.cur.fetchall()
            if (len(price)): found = True
            else: _datetime = _datetime - timedelta(days=1)

        return(price[0][0]) #We just retrieved a number but it's inside a list of tuples, so we must present it as a single float   