from .IndicatorGenBase import IndicatorGenBase

class VWapIndicatorGen(IndicatorGenBase):
    def __init__(self, timePeriodMinutes):
        super().__init__(timePeriodMinutes)
        self.average = 0
        self.volume = 0

    def StartNewTimePeriod(self):
        self.volume = 0

    def ProcessTransation(self, time, amount, price):
        self.average = ((self.average * self.volume) + (price * abs(amount))) / (self.volume + abs(amount))
        self.volume += abs(amount)

    def GetIndicatorValues(self):
        return {"vwap" : self.average}