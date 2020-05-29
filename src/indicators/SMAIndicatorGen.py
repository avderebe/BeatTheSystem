from .SlidingWindowIndicatorBase import *
from datetime import timedelta

class SMAIndicatorGen(SlidingWindowIndicatorBase):
    def __init__(self, timePeriod):
        super().__init__(timePeriod)
        self.windowAverage = 0
        self.windowCount = 0
        self.average = 0
        self.count = 0
        
        days = self.timePeriod.days
        hrs = round(self.timePeriod.seconds / 3600,1)
        minutes = round(self.timePeriod.seconds / 60)
        self.indicator = str(days) + "daySMA" if days != 0 else str(hrs) + "hrSMA" if hrs >= 1 else str(minutes) + "minSMA"


    def CreateEntry(self):
        avg = self.average
        cnt = self.count
        self.average = 0
        self.count = 0
        return {'average' : avg, 'count' : cnt}

    def ProcessAddition(self, entry):
        self.windowAverage = (self.windowAverage * self.windowCount + entry['average'] * entry['count']) / (self.windowCount + entry['count'])
        self.windowCount = self.windowCount + entry['count']

    def ProcessRemoval(self, entry):
        try:
            self.windowAverage = (self.windowAverage * self.windowCount - entry['average'] * entry['count']) / (self.windowCount - entry['count'])
            self.windowCount = self.windowCount - entry['count']
        except:
            self.windowAverage = 0
            self.windowCount = 0

    def ProcessTransation(self, time, amount, price):
        self.average = (self.average * self.count + price) / (self.count + 1)
        self.count = self.count + 1

    def GetIndicatorValues(self):
        return {self.indicator : (self.average * self.count + self.windowAverage * self.windowCount) / (self.count + self.windowCount)}