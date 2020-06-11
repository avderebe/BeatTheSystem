from datetime import timedelta

class IndicatorGenBase:
    def __init__(self, timePeriod):
        self.timePeriod = timePeriod
        self.timeElapsed = timedelta()

    def StartNewTimePeriod(self):
        return

    def AdvanceTime(self, time):
        self.timeElapsed += time
        while self.timeElapsed >= self.timePeriod:
            self.timeElapsed -= self.timePeriod
            self.StartNewTimePeriod()

    def ProcessTransation(self, time, amount, price):
        return

    def GetIndicatorValues(self):
        return {}

    #need to make sure that derived classes do not share the same state variables
    def GetState(self):
        return {}

    def LoadState(self, data):
        return