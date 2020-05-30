from .IndicatorGenBase import *
from datetime import timedelta

class SlidingWindowIndicatorBase(IndicatorGenBase):
    def __init__(self, timePeriod):
        super().__init__(timePeriod)
        self.runningTime = timedelta()
        self.window = []


    #Say the underlying code calls advance time every 5 minutes, but the whole time period 
    #of this indicator is 1 day
    #Each entry in the window consists of 5 minutes of data
    #but we will keep the last day's worth of entries
    #So we process and remove an entry every time we advance time
    def AdvanceTime(self, time):
        entry = self.CreateEntry()
        self.window.append({'time': self.runningTime, 'entry': entry})
        self.runningTime += time
        self.ProcessAddition(entry)

        while (len(self.window) != 0 and self.runningTime - self.window[0]['time'] >= self.timePeriod):
            self.ProcessRemoval(self.window[0]['entry'])
            self.window = self.window[1:]

    def CreateEntry(self):
        return {}

    def ProcessAddition(self, entry):
        return

    def ProcessRemoval(self, entry):
        return
