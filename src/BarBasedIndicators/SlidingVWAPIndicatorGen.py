from .SlidingWindowIndicatorBase import *
from datetime import timedelta
from decimal import Decimal

class SlidingVWAPIndicatorGen(SlidingWindowIndicatorBase):
    def __init__(self, timePeriod):
        super().__init__(timePeriod)
        #hold both window average and running average for current time period
        self.windowAverage = 0
        self.windowVolume = 0
        

        #annoying but correct way to round 0's off numbers
        DropZeros = lambda d : d.to_integral() if d == d.to_integral() else d.normalize()

        days = self.timePeriod.days
        hrs = round(self.timePeriod.seconds / 3600,1)
        minutes = round(self.timePeriod.seconds / 60)
        self.indicator = str(days) + "daySVWAP" if days != 0 else str(DropZeros(Decimal(hrs))) + "hrSVWAP" if hrs >= 1 else str(DropZeros(Decimal(minutes))) + "minSVWAP"


    def CreateEntry(self, bar):
        return {'volume' : bar['vtotal'],  'average' : bar['vwap']}

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

    def GetIndicatorValues(self):
        return {self.indicator : self.windowAverage}