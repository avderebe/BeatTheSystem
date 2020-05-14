from .IndicatorGenBase import IndicatorGenBase
from datetime import *

class VWapIndicatorGen(IndicatorGenBase):
    def __init__(self, timePeriodMinutes):
        super().__init__(timePeriodMinutes)
        self.average = 0
        self.volume = 0
        self.day = 1

    def StartNewTimePeriod(self, time):
        if (self.day != time.day):
            self.volume = 0
            self.day = time.day

    def ProcessTransation(self, time, amount, price):
        self.average = ((self.average * self.volume) + (price * abs(amount))) / (self.volume + abs(amount))
        self.volume += abs(amount)

    def GetIndicatorValues(self):
        return {"vwap" : self.average}