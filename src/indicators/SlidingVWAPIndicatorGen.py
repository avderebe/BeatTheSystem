from .SlidingWindowIndicatorBase import *
from datetime import timedelta
from decimal import Decimal

class SlidingVWAPIndicatorGen(SlidingWindowIndicatorBase):
    def __init__(self, timePeriod):
        super().__init__(timePeriod)
        #hold both window average and running average for current time period
        self.windowAverage = 0
        self.windowVolume = 0
        self.average = 0
        self.volume = 0
        
        days = self.timePeriod.days
        hrs = round(self.timePeriod.seconds / 3600,1)
        minutes = round(self.timePeriod.seconds / 60)
        self.indicator = str(days) + "daySVWAP" if days != 0 else str(Decimal(hrs).normalize()) + "hrSVWAP" if hrs >= 1 else str(Decimal(minutes).normalize()) + "minSVWAP"


    def CreateEntry(self):
        vol = self.volume
        avg = self.average
        self.average = 0
        self.volume = 0
        return {'volume' : vol,  'average' : avg}

    def ProcessAddition(self, entry):
        self.windowAverage = (self.windowAverage * self.windowVolume + entry['average'] * entry['volume']) / (self.windowVolume + entry['volume'])
        self.windowVolume = self.windowVolume + entry['volume']

    def ProcessRemoval(self, entry):
        try:
            self.windowAverage = (self.windowAverage * self.windowVolume - entry['average'] * entry['volume']) / (self.windowVolume - entry['volume'])
            self.windowVolume = self.windowVolume - entry['volume']
        except:
            #wont happen unless you're doing a 5 min sliding vwap with a 5 minute bar gen
            self.windowAverage = 0
            self.windowVolume = 0

    def ProcessTransation(self, time, amount, price):
        self.average = ((self.average * self.volume) + (price * abs(amount))) / (self.volume + abs(amount))
        self.volume += abs(amount)

    def GetIndicatorValues(self):
        return {self.indicator : (self.average * self.volume + self.windowAverage * self.windowVolume)/(self.volume + self.windowVolume)}