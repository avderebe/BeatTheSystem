from .IndicatorGenBase import IndicatorGenBase
from enum import Enum

class VolumeType(Enum):
    Buy = 1
    Sell = 2
    All = 3


class VolumeIndicatorGen(IndicatorGenBase):
    def __init__(self, timePeriod, volumeType):
        super().__init__(timePeriod)
        self.Type = volumeType
        self.volume = 0

        if self.Type == VolumeType.Buy:
            self.indicator = "vbuy"
        elif self.Type == VolumeType.Sell:
            self.indicator = "vsell"
        elif self.Type == VolumeType.All:
            self.indicator = "vtotal"

    def StartNewTimePeriod(self):
        self.volume = 0

    def ProcessTransation(self, time, amount, price):
        if self.Type == VolumeType.Buy and amount >= 0:
            self.volume += abs(amount)
        elif self.Type == VolumeType.Sell and amount <= 0:
            self.volume += abs(amount)
        elif self.Type == VolumeType.All:
            self.volume += abs(amount)

    def GetIndicatorValues(self):
        return {self.indicator : self.volume}

    def GetState(self):
        return {self.indicator : {'volume' : self.volume}}

    def LoadState(self, data):
        self.volume =  data[self.indicator]['volume']