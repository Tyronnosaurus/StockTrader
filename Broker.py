from FinancialData.DataReader import DataReader
from datetime import datetime


class SharesGroup:
    def __init__(self, _tkr, _qty, _price):
        self.ticker = _tkr
        self.quantity = _qty
        self.buyPrice = _price



class Broker:
    def __init__(self):
        self.currentTime = datetime.now()
        self.Funds = 0
        self.Portfolio = []
        self.dataReader = DataReader()



    def PlaceBuyOrder(self, ticker, quantity, maxValue):
        pass


    def PlaceSellOrder(self, ticker, quantity, minValue):
        pass


    #Buy a group of shares at current market price
    def BuyInstantly(self, ticker, quantity):
        self.Funds -= self.dataReader.GetPrice(ticker, self.currentTime) * quantity
        s = SharesGroup(ticker, quantity, 10)
        self.Portfolio.append(s)


    #Sell the group of shares at position i in portfolio, at the current market price
    def SellInstantly(self, i):
        self.Funds += self.dataReader.GetPrice(self.Portfolio[i].ticker, self.currentTime) * self.Portfolio[i].quantity
        del self.Portfolio[i]     #Delete shares group from portfolio


    def ListPortfolio(self):
        pass


    def LoadFunds(self, newFunds):
        self.Funds += newFunds




