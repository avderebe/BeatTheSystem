from .SlidingWindowIndicatorBase import *
from datetime import timedelta

class SMAIndicatorGen(SlidingWindowIndicatorBase):
    def __init__(self, timePeriod):
        super().__init__(timePeriod)
        self.average = 0
        self.n = 0
        
        days = self.timePeriod.days
        hrs = round(self.timePeriod.seconds / 3600,1)
        minutes = round(self.timePeriod.seconds / 60)
        self.indicator = str(days) + "daySMA" if days != 0 else str(hrs) + "hrSMA" if hrs >= 1 else str(minutes) + "minSMA"


    def CreateEntry(self, time, amount, price):
        return {'price' : price}

    def ProcessAddition(self, entry):
        self.average = (self.average * self.n + entry['price']) / (self.n + 1)
        self.n = self.n + 1

    def ProcessRemoval(self, entry):
        self.average = (self.average * self.n - entry['price']) / (self.n - 1)
        self.n = self.n - 1

    def GetIndicatorValues(self):

        return {self.indicator : self.average}