import sqlite3
from datetime import datetime, date
import os


class DataReader:
    
    def __init__(self):
        workDir = os.getcwd()
        self.conn = sqlite3.connect(workDir + '/FinancialData/StockDB.db')
        self.cur = self.conn.cursor()


    def GetPrice(self, ticker, datetime):
        self.cur.execute("SELECT Close FROM '%s' WHERE Date = '%s'" % (ticker, datetime))
        price = self.cur.fetchall()
        return(price)
