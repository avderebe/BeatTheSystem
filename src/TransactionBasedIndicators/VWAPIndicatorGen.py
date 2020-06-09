from .IndicatorGenBase import IndicatorGenBase
from datetime import *
from decimal import Decimal

#do not use this VWAP gen for generating data that spans multiple bars
#This one will only span the one bar
class VWapIndicatorGen(IndicatorGenBase):
    def __init__(self, timePeriod):
        super().__init__(timePeriod)
        self.average = 0
        self.volume = 0

    def StartNewTimePeriod(self):
            self.volume = 0

    def ProcessTransation(self, time, amount, price):
        self.average = ((self.average * self.volume) + (price * abs(amount))) / (self.volume + abs(amount))
        self.volume += abs(amount)

    def GetIndicatorValues(self):
        return {"vwap": self.average}