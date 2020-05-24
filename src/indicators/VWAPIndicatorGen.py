from .IndicatorGenBase import IndicatorGenBase
from datetime import *

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
        return {"vwap" : self.average}