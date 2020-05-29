from .IndicatorGenBase import IndicatorGenBase
from datetime import *
from decimal import Decimal

class VWapIndicatorGen(IndicatorGenBase):
    def __init__(self, timePeriod):
        super().__init__(timePeriod)
        self.average = 0
        self.volume = 0
        
        days = self.timePeriod.days
        hrs = round(self.timePeriod.seconds / 3600,1)
        minutes = round(self.timePeriod.seconds / 60)
        self.indicator = str(days) + "dayVWAP" if days != 0 else str(Decimal(hrs).normalize()) + "hrVWAP" if hrs >= 1 else str(Decimal(minutes).normalize()) + "minVWAP"

    def StartNewTimePeriod(self):
            self.volume = 0

    def ProcessTransation(self, time, amount, price):
        self.average = ((self.average * self.volume) + (price * abs(amount))) / (self.volume + abs(amount))
        self.volume += abs(amount)

    def GetIndicatorValues(self):
        return {self.indicator : self.average}