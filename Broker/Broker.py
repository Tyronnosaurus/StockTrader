from DbReader.DbReader import DbReader
from datetime import datetime
from .Order import Order, buySell, limitTypes, timeTypes
from .SharesGroup import SharesGroup



class Broker:
    def __init__(self):
        self.currentTime = datetime.now()
        self.Funds = 0.0
        self.Portfolio = []
        self.Orders = []
        self.dbReader = DbReader()



    def PlaceOrder(self, buySell, limitType, ticker, quantity, price):
        order = Order(buySell, limitType, price, ticker, quantity, 0, timeTypes.PERMANENT)
        self.Orders.append(order)


    def ExecuteOrders(self):
        for i,order in enumerate(self.Orders):
            if (self._canBeExecuted(order)):
                self._executeOrder(order)
                del self.Orders[i]  #Delete order once executed
       

    #Returns True if order can be executed according to its limits and the current market price
    def _canBeExecuted(self, order):
        if (order.limitType == limitTypes.MARKET): return(True)
        if (order.limitType == limitTypes.LIMITED):
            if   (order.buySell == buySell.BUY)  and (self.dbReader.GetPrice(order.productId, self.currentTime) <= order.price): return(True)
            elif (order.buySell == buySell.SELL) and (self.dbReader.GetPrice(order.productId, self.currentTime) >= order.price): return(True)


    #Executes an order
    def _executeOrder(self, order):
        if   (order.buySell == buySell.BUY):  self._buyInstantly(order)
        elif (order.buySell == buySell.SELL): self._sellInstantly(order)


    #Buy a group of shares at current market price
    def _buyInstantly(self, order):
        #Get current market price and take money out of the funds to buy the shares
        marketPrice = self.dbReader.GetPrice(order.productId, self.currentTime)
        self.Funds -= marketPrice * order.size
        #Add a shareGroup to the portfolio
        s = SharesGroup(order.productId, order.size, marketPrice, self.currentTime)
        self.Portfolio.append(s)

        logTxt = "    BUY {:8} {} x ${:.2f} = -${:.2f}"
        print(logTxt.format(order.productId, order.size, marketPrice, order.size*marketPrice)) 


    #Sell shares from portfolio at the current market price
    def _sellInstantly(self, order):

        #First, make sure there are enough shares to sell
        if (not self._haveEnoughSharesInPortfolio(order)):
            print("Order: %s x %s failed: not enough shares in portfolio" % (order.productId, order.size))
            for item in self.Portfolio: print(item.ticker, item.quantity)
        else:
            remainingQtyToSell = order.size
            marketPrice = self.dbReader.GetPrice(order.productId, self.currentTime)
            for i,sharesGroup in enumerate(self.Portfolio):
                if (sharesGroup.ticker == order.productId):
                    if (remainingQtyToSell >= sharesGroup.quantity):
                        self.Funds += marketPrice * self.Portfolio[i].quantity
                        del self.Portfolio[i]     #Delete shares group from portfolio
                        remainingQtyToSell -= sharesGroup.quantity
                    elif (remainingQtyToSell < sharesGroup.quantity):
                        self.Funds += marketPrice * remainingQtyToSell
                        self.Portfolio[i].ReduceQtyBy(remainingQtyToSell)
                        remainingQtyToSell = 0
                        break   #Exit the 'for' loop
        
        logTxt = "    SELL {:8} {} x ${:.2f} = +${:.2f}"
        print(logTxt.format(order.productId, order.size, marketPrice, order.size*marketPrice)) 



    def _haveEnoughSharesInPortfolio(self, order):
        sharesFound = 0
        for _,sharesGroup in enumerate(self.Portfolio):
            if (sharesGroup.ticker == order.productId):
                sharesFound += sharesGroup.quantity
                if (sharesFound >= order.size): return(True)
        return(False)


    def ListPortfolio(self):
        pass


    def calculateSharesValue(self):
        sharesValue = 0
        for group in self.Portfolio:
             sharesValue += group.quantity * self.dbReader.GetPrice(group.ticker, self.currentTime)
        return(sharesValue)


    def GetAccountValue(self):
        return(self.calculateSharesValue() + self.Funds)


    def ShowAccountValue(self):
        sharesValue = self.calculateSharesValue()
        totalValue = self.Funds + sharesValue
        print('RESULTS ({}): Funds ${:.2f}  |  Stocks ${:.2f}  |  Total ${:.2f}'.format(self.currentTime, self.Funds, sharesValue, totalValue))


    def LoadFunds(self, newFunds):
        self.Funds += newFunds


    def SetDateTime(self, dt):
        self.currentTime = dt


    #Returns True if we already have stocks from a certain company in our portfolio
    def AlreadyHaveStocksFrom(self, ticker):
        for item in self.Portfolio:
            if(item.ticker == ticker): return(True)
        return(False)


