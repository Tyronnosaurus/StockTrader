from Broker.Broker import Broker
from Broker.Order import buySell, limitTypes
from datetime import date, timedelta
from Helpers import daterange, datetime
import matplotlib.pyplot as plt
from DbReader.DbReader import DbReader

Indexes = ['GDAXI',    #DAX
           'MDAXI',    #MDAX
           'IBEX']     #IBEX 35

class Simulator:

    def __init__(self, Start_date, End_date):
        self.start_date = Start_date
        self.end_date   = End_date
        self.broker = Broker()       #Stores our funds and portfolio, executes buy&sell orders   
        self.dbReader = DbReader() #Connects to SQL and fetches information


    def RunSimulation(self):
        self.broker.LoadFunds(25000.0)
        self.dailyAccountValue = []  #Used to graph results over time

        for t in daterange(self.start_date, self.end_date):
            self.broker.SetDateTime(t)    #Change broker's internal time so that it looks at past price data

            SingleInvestment = 2000  #Spend up to this for each buy 

            ## STRATEGY ##
            #If funds > $SingleInvestment
            if (self.broker.Funds >= SingleInvestment):

                for index in Indexes:
                    #Find an index that is lowish (don't want to buy stocks while market is high)
                    if(self.dbReader.IsLow(index, t, 5, 0.3)):

                        #Get list of stocks in that index
                        usableStocks = self.dbReader.GetStocksInIndex(index)

                        for ticker in usableStocks:
                            #Find a stock in local min, 1Y-5Y low-ish
                            if(not self.broker.AlreadyHaveStocksFrom(ticker) and    #Diversify! Don't buy stocks we already have
                                self.dbReader.IsLow(ticker, t, 5, 0.05) and          #Clear week low
                                self.dbReader.IsLow(ticker, t, 500, 0.25)):          #2 year low-ish

                                if (self.broker.Funds >= SingleInvestment):
                                    #Buy instantaneously
                                    currPrice = self.dbReader.GetPrice(ticker, t)
                                    qty = int(SingleInvestment/currPrice) #Can't buy partial stocks, so use int()
                                    self.broker.PlaceOrder(buySell.BUY, limitTypes.MARKET, ticker, qty , 0)

                                    #Place Sell Order for 102% of buy price
                                    sellPrice = currPrice*1.02
                                    self.broker.PlaceOrder(buySell.SELL, limitTypes.LIMITED, ticker, qty, sellPrice)
                                    
                                    self.broker.ExecuteOrders() #Must execute after every buy order, or else funds aren't substracted immediately


            #Sell at a loss stocks that are keeping cash hostage
            for item in self.broker.Portfolio:
                print(t - item.buyTime)
                if(t - item.buyTime > timedelta(days=10)):
                    print("Gonna sell old stock {}".format(item.ticker))
                    self.broker.PlaceOrder(buySell.SELL, limitTypes.MARKET, item.ticker, item.quantity, 0)
                    self.broker.ExecuteOrders()

            #Command trader to execute any buy&sell orders
            self.broker.ExecuteOrders()
            self.dailyAccountValue.append(self.broker.GetAccountValue())

            self.broker.ShowAccountValue()
        
        self.ShowResults()





    def ShowResults(self):
        self.broker.ShowAccountValue()

        ##Plot value over time
        plt.plot(self.dailyAccountValue)
        plt.show()



start_date = datetime(2018, 1, 1, 0, 0, 0)
end_date   = datetime(2020, 1, 1, 0, 0, 0)
simulator = Simulator(start_date, end_date)
simulator.RunSimulation()