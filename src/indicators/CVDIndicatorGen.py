from .VolumeIndicatorGen import *
from .IndicatorGenBase import IndicatorGenBase

class CVDIndicatorGen(IndicatorGenBase):
    def __init__(self, timePeriod):
        super().__init__(timePeriod)
        self.delta = VolumeIndicatorGen(timePeriod, VolumeType.DeltaCVD)
        self.open = None
        self.close = None
        self.low = None
        self.high = None

    def StartNewTimePeriod(self):
        self.open = self.close
        self.low = self.close
        self.high = self.close

    def ProcessTransation(self, time, amount, price):
        self.delta.ProcessTransation(time, amount, price)
        if self.open is None:
            self.open = self.delta.volume
            self.low = self.delta.volume
            self.high = self.delta.volume
        
        if self.low > self.delta.volume:
            self.low = self.delta.volume
        
        if self.high < self.delta.volume:
            self.high = self.delta.volume
        
        self.close = self.delta.volume

    def GetIndicatorValues(self):
        return {'CVDo' : self.open, 'CVDc' : self.close, 'CVDl' : self.low, 'CVDh' : self.high}