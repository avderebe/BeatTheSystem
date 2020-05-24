#importing just the class from IndicatorGenBase module
from indicators.IndicatorGenBase import IndicatorGenBase

import math


class BarChartIndicatorGen(IndicatorGenBase):
    def __init__(self, timePeriod):
        #initialize the super class (This is the class that gives the basic structure of the indicator generator)
        super().__init__(timePeriod)
        self.open = None
        self.close = None
        self.low = None
        self.high = None
        self.direction = None
        self.h1 = None
        self.h2 = None
        self.l1 = None
        self.l2 = None
        self.l1time = None
        self.l2time = None
        self.h1time = None
        self.h2time = None
        self.trend = 1
        self.prev = 0
        self.lasttime = None

    def StartNewTimePeriod(self):
        #sets everything to values from last bar chart
        self.open = self.close
        self.low = self.close
        self.high = self.close

    def ProcessTransation(self, time, amount, price):
        if self.open is None:
            self.direction = 0
            self.prev = 0
            self.open = price
            self.low = price
            self.high = price
        
        if self.low > price:
            self.low = price
        
        if self.high < price:
            self.high = price
        
        self.close = price
        self.lasttime = time

    def GetIndicatorValues(self):
        #if up candle
        if  self.close > self.open:
            self.direction = 1

            if self.l2 == None:
                self.l2 = self.open
                self.l2time = self.lasttime
            if self.h1 == None:
                if self.h2 and self.close > self.h2:
                    if self.trend == 1:
                        self.h2 = self.close
                        self.h1 = None
                        if self.l1:
                            self.l2 = self.l1
                            self.l1 = None
                        print("up continuation@@@@@@@@@@@@@@@@@")
                    if self.trend == 0:
                        self.h2 = self.close
                else:
                    self.h1 = self.close
                    self.h1time = self.lasttime
            if self.h1 and self.close > self.h1:
                if self.prev == 0:
                    if self.trend == 1:
                        self.l2 = self.l1
                        self.l2time = self.l1time
                        self.l1 = None
                        self.l1time = None
                self.h1 = self.close
                self.h1time = self.lasttime
                if self.h2 and self.h1 >= self.h2:
                    self.trend = 1
                    self.h2 = self.h1
                    self.h1 = None
                    if self.l1:
                        self.l2 = self.l1
                        self.l1 = None
                    print("uptrend@@@@@@@@@@@@@@@@@@@@@@@@@@@")
            self.prev = 1

        #if down candle
        if  self.close < self.open:
            self.direction = 0

            if self.h2 == None:
                self.h2 = self.open
                self.h2time = self.lasttime
            if self.l1 == None:
                if self.l2 and self.close < self.l2:
                    if self.trend == 0:
                        self.l2 = self.close
                        self.l1 = None
                        if self.h1:
                            self.h2 = self.h1
                            self.h1 = None
                        print("down continuation@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
                    if self.trend == 1:
                        self.l2 = self.close
                else:
                    self.l1 = self.close
                    self.l1time = self.lasttime
            if self.l1 and self.close < self.l1:
                if self.prev == 1:
                    if self.trend == 0:
                        self.h2 = self.h1
                        self.h2time = self.h1time
                        self.h1 = None
                        self.h1time = None
                self.l1 = self.close
                self.l1time = self.lasttime
                if self.l2 and self.l1 <= self.l2:
                    self.trend = 0
                    self.l2 = self.l1
                    self.l1 = None
                    if self.h1:
                        self.h2 = self.h1
                        self.h1 = None
                    print("downtrend@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")

            self.prev = 0
                    
        return {'direction' : self.direction, 'trend' : self.trend,  'h1' : self.h1, 'l1' : self.l1, 'h2' : self.h2, 'l2' : self.l2, 'open' : self.open, 'close' : self.close, 'low' : self.low, 'high' : self.high,'l1time' : self.l1time, 'h1time' : self.h1time, 'l2time' : self.l2time, 'h2time' : self.h2time}
