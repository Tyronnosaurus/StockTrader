from Broker.Broker import Broker
from Broker.Order import buySell, limitTypes
from datetime import date
from Helpers import daterange, datetime
import matplotlib.pyplot as plt
from DbReader.DbReader import DbReader


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



            ## STRATEGY ##
            #If funds > $5000
            if (self.broker.Funds >= 5000):
                pass
                #Get list of indexes
                #Find an index with a local min. Return if not found
                index = 'GDAXI'

                #Get list of stocks in that index
                usableStocks = self.dbReader.GetStocksInIndex(index)

                #Find a stock in local min, 1Y-5Y low-ish
                
                #Buy $5000 of it instantaneously
                #Place Sell Order for 102% of buy price

            #Command trader to execute any buy&sell orders

            if (t.day == 10): self.broker.PlaceOrder(buySell.BUY, limitTypes.MARKET, 'ADS.DE', 5, 0)

            self.broker.ExecuteOrders()
            self.dailyAccountValue.append(self.broker.GetAccountValue())

        self.ShowResults()





    def ShowResults(self):
        self.broker.ShowAccountValue()

        ##Plot value over time
        plt.plot(self.dailyAccountValue)
        plt.show()



start_date = datetime(2019, 1, 1, 0, 0, 0)
end_date   = datetime(2020, 1, 1, 0, 0, 0)
simulator = Simulator(start_date, end_date)
simulator.RunSimulation()