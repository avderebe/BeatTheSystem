from .SlidingWindowIndicatorBase import *
from datetime import timedelta
from decimal import Decimal
import math

class SlidingVWAPIndicatorGen(SlidingWindowIndicatorBase):
    def __init__(self, timePeriod):
        super().__init__(timePeriod)
        #hold both window average and running average for current time period
        self.windowAverage = 0
        self.windowVolume = 0
        self.windowVariance = 0
        self.svwap = 0
        self.average = 0
        self.volume = 0
        self.variance = 0
        
        days = self.timePeriod.days
        hrs = round(self.timePeriod.seconds / 3600,1)
        minutes = round(self.timePeriod.seconds / 60)
        self.indicator = str(days) + "daySVWAP" if days != 0 else str(Decimal(hrs).normalize()) + "hrSVWAP" if hrs >= 1 else str(Decimal(minutes).normalize()) + "minSVWAP"


    def CreateEntry(self):
        vol = self.volume
        avg = self.average
        var = self.variance
        self.average = 0
        self.volume = 0
        self.variance = 0
        return {'volume' : vol,  'average' : avg, 'variance' : var}

    def ProcessAddition(self, entry):
        self.windowAverage = (self.windowAverage * self.windowVolume + entry['average'] * entry['volume']) / (self.windowVolume + entry['volume'])
        self.windowVolume = self.windowVolume + entry['volume']
        self.windowVariance = self.windowVariance + entry['variance']

    def ProcessRemoval(self, entry):
        try:
            self.windowAverage = (self.windowAverage * self.windowVolume - entry['average'] * entry['volume']) / (self.windowVolume - entry['volume'])
            self.windowVolume = self.windowVolume - entry['volume']
            self.windowVariance = self.windowVariance - entry['variance']
        except:
            #wont happen unless you're doing a 5 min sliding vwap with a 5 minute bar gen
            self.windowAverage = 0
            self.windowVolume = 0
            self.windowVariance = 0

    def ProcessTransation(self, time, amount, price):
        self.average = ((self.average * self.volume) + (price * abs(amount))) / (self.volume + abs(amount))
        self.volume += abs(amount)
        self.svwap = (self.average * self.volume + self.windowAverage * self.windowVolume)/(self.volume + self.windowVolume)
        self.variance = (price-self.svwap)**2

    def GetIndicatorValues(self):
        if self.windowFull is True:
            sigma = math.sqrt((self.variance+self.windowVariance)/len(self.window))
        else:
            sigma = math.sqrt((self.variance+self.windowVariance)/(len(self.window)+1))

        return {self.indicator : self.svwap, self.indicator+"_sigma" : sigma}