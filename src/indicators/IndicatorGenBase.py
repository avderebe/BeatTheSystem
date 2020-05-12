
class IndicatorGenBase:
    def __init__(self, timePeriodMinutes):
        self.timePeriodMinutes = timePeriodMinutes

    def StartNewTimePeriod(self):
        return

    def ProcessTransation(self, time, amount, price):
        return

    def GetIndicatorValues(self):
        return {}