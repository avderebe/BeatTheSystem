#importing just the class from IndicatorGenBase module
from indicators.IndicatorGenBase import IndicatorGenBase
from indicators.BarChartIndicatorGen import BarChartIndicatorGen

import math


class MarketStructureIndicatorGen(IndicatorGenBase):
    def __init__(self, timePeriod):
        #initialize the super class (This is the class that gives the basic structure of the indicator generator)
        super().__init__(timePeriod)
        self.barChart = BarChartIndicatorGen(timePeriod)
        self.direction = None
        self.trend = 0.5
        self.h1 = None
        self.h2 = None
        self.h3 = None
        self.l1 = None
        self.l2 = None
        self.l3 = None
        self.cont = 0
        self.prev = None

    def AdvanceTime(self, time):
        self.timeElapsed += time
        while self.timeElapsed >= self.timePeriod:
            self.timeElapsed -= self.timePeriod
            self.barChart.AdvanceTime(time)
        
    def ProcessTransation(self, time, amount, price):
        self.barChart.ProcessTransation(time, amount, price)

    def GetIndicatorValues(self):
        self.cont = None
        #if up candle
        if  self.barChart.close > self.barChart.open:
            self.direction = 1
            #init first bar
            if self.prev is None:
                self.l2 = self.barChart.open
                self.h1 = self.barChart.close
            #if (close above ceiling)
            if (self.h2 and self.barChart.close > self.h2):
                self.l1 = None
                self.l2 = None
                self.h1 = self.barChart.close
                self.h2 = None
                if self.trend == 1:
                    self.cont = 1
                self.trend = 1
            #if no local high, now we do have one
            if self.h1 == None:
                self.h1 = self.barChart.close
            #if there is a local high, and we made a lower high, set floor
            if self.h1 and self.barChart.close < self.h1:
                if self.l1:
                    self.l2 = self.l1
                self.h1 = self.barChart.close
            #if we have a high, lower high, and a low, set floor
            if self.h2 and (self.h1 < self.h2) and self.l1:
                self.l2 = self.l1
                self.l1 = None
            #if a higher local high has formed
            if self.barChart.close > self.h1:
                self.h1 = self.barChart.close

            self.prev = 1
        #############################################
        #if down candle
        if  self.barChart.close < self.barChart.open:
            self.direction = 0
            #init first bar
            if self.prev is None:
                self.h2 = self.barChart.open
                self.l1 = self.barChart.close
            #if (close below floor)
            if (self.l2 and self.barChart.close < self.l2):
                if self.trend == 0:
                    self.cont = -1
                self.trend = 0
                self.l1 = self.barChart.close
                self.l2 = None
                self.h1 = None
                self.h2 = None
            #if no local low, now we do have one
            if self.l1 == None:
                self.l1 = self.barChart.close
            #if there is a local low, and we made a higher low, set ceiling
            if self.l1 and self.barChart.close > self.l1:
                if self.h1:
                    self.h2 = self.h1
                self.l1 = self.barChart.close
            #if we have a low, higher low, and a high, set the high as the ceiling
            if self.l2 and (self.l1 > self.l2) and self.h1:
                self.h2 = self.h1
                self.h1 = None
            #if a lower local lower has formed
            if self.barChart.close < self.l1:
                self.l1 = self.barChart.close

        self.prev = 0
                    
        return {'direction' : self.direction, 'trend' : self.trend,  'h1' : self.h1, 'l1' : self.l1, 'h2' : self.h2, 'l2' : self.l2, 'l3' : self.l3, 'cont' : self.cont}
