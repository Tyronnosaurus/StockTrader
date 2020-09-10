from FinancialData.DataReader import DataReader
from datetime import datetime


class SharesGroup:
    def __init__(self, _tkr, _qty, _price):
        self.ticker = _tkr
        self.quantity = _qty
        self.buyPrice = _price



class BuyOrder:
    def __init__(self, _tkr, _qty, _maxPrice):
        self.Ticker = _tkr
        self.Quantity = _qty
        self.MaxPrice = _maxPrice

class SellOrder:
    def __init__(self, _tkr, _qty, _minPrice):
        self.Ticker = _tkr
        self.Quantity = _qty
        self.MinPrice = _minPrice




class Broker:
    def __init__(self):
        self.currentTime = datetime.now()
        self.Funds = 0.0
        self.Portfolio = []
        self.BuyOrders = []
        self.SellOrders = []
        self.dataReader = DataReader()



    def PlaceBuyOrder(self, ticker, quantity, maxPrice):
        self.BuyOrders.append(BuyOrder(ticker, quantity, maxPrice))


    def PlaceSellOrder(self, ticker, quantity, minPrice):
        self.SellOrders.append(SellOrder(ticker, quantity, minPrice))

    def ExecuteOrders(self):
        for buyOrder,i in enumerate(self.BuyOrders):
            if (self.dataReader.GetPrice(buyOrder.ticker, self.currentTime) <= buyOrder.maxPrice):
                self.BuyInstantly(buyOrder.ticker, buyOrder.quantity)
                del self.SellOrders[i]
        
        for sellOrder,i in (self.SellOrders):
            if (self.dataReader.GetPrice(sellOrder.ticker, self.currentTime) >= sellOrder.minPrice):
                self.SellInstantly(sellOrder.ticker, sellOrder.quantity)
                del self.BuyOrders[i]


    #Buy a group of shares at current market price
    def BuyInstantly(self, ticker, quantity):
        self.Funds -= self.dataReader.GetPrice(ticker, self.currentTime) * quantity
        s = SharesGroup(ticker, quantity, 10)
        self.Portfolio.append(s)


    #Sell a group of shares from portfolio at the current market price
    #(only entire groups can be sold for now)
    def SellInstantly(self, ticker, quantity):
        for sharesGroup, i in enumerate(self.Portfolio):
            if (sharesGroup.ticker == ticker and sharesGroup.quantity == quantity):
                self.Funds += self.dataReader.GetPrice(self.Portfolio[i].ticker, self.currentTime) * self.Portfolio[i].quantity
                del self.Portfolio[i]     #Delete shares group from portfolio


    def ListPortfolio(self):
        pass


    def calculateSharesValue(self):
        sharesValue = 0
        for group in self.Portfolio:
             sharesValue += group.quantity * self.dataReader.GetPrice(group.ticker, self.currentTime)
        return(sharesValue)


    def GetAccountValue(self):
        return(self.calculateSharesValue() + self.Funds)


    def ShowAccountValue(self):
        sharesValue = self.calculateSharesValue()
        print('Funds: $' + str(self.Funds))
        print('Stocks:$' + str(sharesValue))
        print('Total: $' + str(self.Funds + sharesValue))


    def LoadFunds(self, newFunds):
        self.Funds += newFunds


    def SetDateTime(self, dt):
        self.currentTime = dt


