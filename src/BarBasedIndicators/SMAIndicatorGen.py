from .SlidingWindowIndicatorBase import *
from datetime import timedelta
from decimal import Decimal

class SMAIndicatorGen(SlidingWindowIndicatorBase):
    def __init__(self, timePeriod):
        super().__init__(timePeriod)
        self.windowAverage = 0
        self.windowCount = 0
        

        #annoying but correct way to round 0's off numbers
        DropZeros = lambda d : d.to_integral() if d == d.to_integral() else d.normalize()

        days = self.timePeriod.days
        hrs = round(self.timePeriod.seconds / 3600,1)
        minutes = round(self.timePeriod.seconds / 60)
        self.indicator = str(days) + "daySMA" if days != 0 else str(DropZeros(Decimal(hrs))) + "hrSMA" if hrs >= 1 else str(DropZeros(Decimal(minutes))) + "minSMA"


    def CreateEntry(self, bar):
        #currently broken until we add a basic count & average to transaction based indicators
        #I dunno if we even need this one anyway
        return {'average' : 0, 'count' : 0}

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

    def GetIndicatorValues(self):
        return {self.indicator : self.windowAverage}