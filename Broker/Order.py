from enum import Enum


class buySell(Enum):
    BUY = 'BUY'
    SELL = 'SELL'

class limitTypes(Enum):
    MARKET = 0           #Execute as quickly as possible, even if there are unexpected price changes
    LIMITED = 1          #Execute at specified price or better, no matter how long it takes
    #STOP_LOSS = 2       #Execute as soon as stopPrice is reached, even if there are unexpected price changes afterwards
    #STOP_LOSS_LIMIT = 3 #Same as STOP_LOSS, but with a limit to prevent excessive losses

class timeTypes(Enum):
    DAY = 1
    PERMANENT = 3


class Order:
    def __init__(self, buySell, limitType, price, productId, size, stopPrice, timeType):
        self.buySell = buySell
        self.limitType = limitType
        self.price = price
        self.productId = productId
        self.size = size
        self.stopPrice = stopPrice
        self.timeType = timeType