#importing just the class from IndicatorGenBase module
from .IndicatorGenBase import IndicatorGenBase
from .BarChartIndicatorGen import BarChartIndicatorGen

import math


class MarketStructureIndicatorGen(IndicatorGenBase):
    def __init__(self, timePeriod):
        #initialize the super class (This is the class that gives the basic structure of the indicator generator)
        super().__init__(timePeriod)
        self.barChart = BarChartIndicatorGen(timePeriod)
        self.pastBars = []

    def AdvanceTime(self, time):
        self.timeElapsed += time
        while self.timeElapsed >= self.timePeriod:
            self.timeElapsed -= self.timePeriod
            self.StartNewTimePeriod()
        
        #advance time for barChart after starting new time period so that you get the open/close before the barchart advancess
        self.barChart.AdvanceTime(time)

    def StartNewTimePeriod(self):
        self.pastBars.append(self.barChart.GetIndicatorValues())
        self.pastBars = self.pastBars[-3:]
        return

    def ProcessTransation(self, time, amount, price):
        self.barChart.ProcessTransation(time, amount, price)

    def GetIndicatorValues(self):
        return self.pastBars
