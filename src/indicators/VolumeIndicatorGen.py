from .IndicatorGenBase import IndicatorGenBase
from enum import Enum

class VolumeType(Enum):
    Buy = 1
    Sell = 2
    All = 3


class VolumeIndicatorGen(IndicatorGenBase):
    def __init__(self, timePeriodMinutes, volumeType):
        super().__init__(timePeriodMinutes)
        self.Type = volumeType
        self.volume = 0

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
        name = ""
        if self.Type == VolumeType.Buy:
            name = "vbuy"
        elif self.Type == VolumeType.Sell:
            name = "vsell"
        elif self.Type == VolumeType.All:
            name = "vtotal"
        return {name : self.volume}