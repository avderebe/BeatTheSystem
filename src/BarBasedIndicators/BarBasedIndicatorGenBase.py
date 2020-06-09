from datetime import timedelta

class BarBasedIndicatorGenBase:
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

    def ProcessBar(self, bar):
        return

    def GetIndicatorValues(self):
        return {}