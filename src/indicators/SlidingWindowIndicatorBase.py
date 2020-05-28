from .IndicatorGenBase import *
from datetime import timedelta

class SlidingWindowIndicatorBase(IndicatorGenBase):
    def __init__(self, timePeriod):
        super().__init__(timePeriod)
        self.window = []

    def AdvanceTime(self, time):
        return

    def CreateEntry(self, time, amount, price):
        return {}

    def ProcessAddition(self, entry):
        return

    def ProcessRemoval(self, entry):
        return

    def ProcessTransation(self, time, amount, price):
        entry = self.CreateEntry(time, amount, price)
        self.window.append({'time': time, 'entry': entry})

        self.ProcessAddition(entry)

        while (len(self.window) != 0 and time - self.window[0]['time'] >= self.timePeriod):
            self.ProcessRemoval(self.window[0]['entry'])
            self.window = self.window[1:]