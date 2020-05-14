#importing just the class from IndicatorGenBase module
from indicators.IndicatorGenBase import IndicatorGenBase

import math


class BarChartIndicatorGen(IndicatorGenBase):
    def __init__(self, timePeriodMinutes):
        #initialize the super class (This is the class that gives the basic structure of the indicator generator)
        super().__init__(timePeriodMinutes)
        self.open = None
        self.close = None
        self.low = None
        self.high = None

    def StartNewTimePeriod(self, time):
        #sets everything to values from last bar chart
        self.open = self.close
        self.low = self.close
        self.high = self.close

    def ProcessTransation(self, time, amount, price):
        if self.open is None:
            self.open = price
            self.low = price
            self.high = price
        
        if self.low > price:
            self.low = price
        
        if self.high < price:
            self.high = price
        
        self.close = price

    def GetIndicatorValues(self):
        return {'open' : self.open, 'close' : self.close, 'low' : self.low, 'high' : self.high}
