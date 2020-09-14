
class SharesGroup:
    def __init__(self, _tkr, _qty, _price, _buyTime):
        self.ticker = _tkr
        self.quantity = _qty
        self.buyPrice = _price
        self.buyTime = _buyTime


    #Method to reduce total amount of shares in a group. Useful when selling only part of the shares
    def ReduceQtyBy(self, numToDecrease):
        self.quantity -= numToDecrease