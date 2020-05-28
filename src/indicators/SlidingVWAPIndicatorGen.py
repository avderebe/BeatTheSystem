from .SlidingWindowIndicatorBase import *
from datetime import timedelta

class SlidingVWAPIndicatorGen(SlidingWindowIndicatorBase):
    def __init__(self, timePeriod):
        super().__init__(timePeriod)
        self.average = 0
        self.volume = 0
        
        days = self.timePeriod.days
        hrs = round(self.timePeriod.seconds / 3600,1)
        minutes = round(self.timePeriod.seconds / 60)
        self.indicator = str(days) + "daySVWAP" if days != 0 else str(hrs) + "hrSVWAP" if hrs >= 1 else str(minutes) + "minSVWAP"


    def CreateEntry(self, time, amount, price):
        return {'amount' : amount,  'price' : price}

    def ProcessAddition(self, entry):
        self.average = (self.average * self.volume + entry['price'] * abs(entry['amount'])) / (self.volume + abs(entry['amount']))
        self.volume = self.volume + abs(entry['amount'])

    def ProcessRemoval(self, entry):
        self.average = (self.average * self.volume - entry['price'] * abs(entry['amount'])) / (self.volume - abs(entry['amount']))
        self.volume = self.volume - abs(entry['amount'])

    def GetIndicatorValues(self):

        return {self.indicator : self.average}