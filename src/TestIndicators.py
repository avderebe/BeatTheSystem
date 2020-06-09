from TransactionBasedIndicators.VolumeIndicatorGen import VolumeType,VolumeIndicatorGen
from TransactionBasedIndicators.BarChartIndicatorGen import BarChartIndicatorGen
from TransactionBasedIndicators.VWAPIndicatorGen import VWapIndicatorGen
from TransactionBasedIndicators.MarketStructureIndicatorGen import MarketStructureIndicatorGen
from BarBasedIndicators.SMAIndicatorGen import SMAIndicatorGen
from BarBasedIndicators.SlidingVWAPIndicatorGen import SlidingVWAPIndicatorGen
from datetime import datetime,timedelta

def TestTranscationBasedIndicators():
    indicatorTimeSpan = timedelta(minutes=5)
    indicators = []
    #indicators.append(SlidingVWAPIndicatorGen(indicatorTimeSpan))
    #indicators.append(SlidingVWAPIndicatorGen(indicatorTimeSpan * 2))
    #indicators.append(SMAIndicatorGen(indicatorTimeSpan))
    #indicators.append(SMAIndicatorGen(indicatorTimeSpan*2))
    indicators.append(BarChartIndicatorGen(indicatorTimeSpan))
    indicators.append(VolumeIndicatorGen(indicatorTimeSpan, VolumeType.Buy))
    indicators.append(VolumeIndicatorGen(indicatorTimeSpan, VolumeType.Sell))
    indicators.append(VolumeIndicatorGen(indicatorTimeSpan, VolumeType.All))
    indicators.append(VWapIndicatorGen(indicatorTimeSpan))
    indicators.append(VWapIndicatorGen(indicatorTimeSpan*3))
    indicators.append(MarketStructureIndicatorGen(indicatorTimeSpan))

    for indicator in indicators:
        dt= datetime.min
        indicator.ProcessTransation(dt.min + 1 * indicatorTimeSpan / 6, 1, 10)
        indicator.ProcessTransation(dt.min + 2 * indicatorTimeSpan / 6, 2, 20)
        indicator.ProcessTransation(dt.min + 3 * indicatorTimeSpan / 6, -1, 5)
        indicator.ProcessTransation(dt.min + 4 * indicatorTimeSpan / 6, -2, 45)
        indicator.ProcessTransation(dt.min + 5 * indicatorTimeSpan / 6, 4, 15)

        print(indicator.GetIndicatorValues())
        indicator.AdvanceTime(indicatorTimeSpan)

        indicator.ProcessTransation(dt.min + 7 * indicatorTimeSpan / 6, -2, 55)
        indicator.ProcessTransation(dt.min + 8 * indicatorTimeSpan / 6, -1, 35)
        indicator.ProcessTransation(dt.min + 9 * indicatorTimeSpan / 6, 3, 45)
        indicator.ProcessTransation(dt.min + 10 * indicatorTimeSpan / 6, -2, 10)
        indicator.ProcessTransation(dt.min + 11 * indicatorTimeSpan / 6, 5, 25)

        print(indicator.GetIndicatorValues())
        indicator.AdvanceTime(indicatorTimeSpan)

        indicator.ProcessTransation(dt.min + 13 * indicatorTimeSpan / 6, 1, 35)
        indicator.ProcessTransation(dt.min + 14 * indicatorTimeSpan / 6, 2, 75)
        indicator.ProcessTransation(dt.min + 15 * indicatorTimeSpan / 6, 3, 65)
        indicator.ProcessTransation(dt.min + 16 * indicatorTimeSpan / 6, 4, 85)
        indicator.ProcessTransation(dt.min + 17 * indicatorTimeSpan / 6, 5, 70)

        print(indicator.GetIndicatorValues())
        indicator.AdvanceTime(indicatorTimeSpan)


def TestBarBasedIndicators():
    indicatorTimeSpan = timedelta(minutes=5)

    indicators = []
    indicators.append(SlidingVWAPIndicatorGen(indicatorTimeSpan))
    indicators.append(SlidingVWAPIndicatorGen(indicatorTimeSpan*2))
    indicators.append(SMAIndicatorGen(indicatorTimeSpan))

    for indicator in indicators:

        indicator.ProcessBar({'vtotal' : 100, 'vwap' : 20})
        print(indicator.GetIndicatorValues())
        indicator.AdvanceTime(indicatorTimeSpan)
        
        indicator.ProcessBar({'vtotal' : 50, 'vwap' : 40})
        print(indicator.GetIndicatorValues())
        indicator.AdvanceTime(indicatorTimeSpan)


        indicator.ProcessBar({'vtotal' : 200, 'vwap' : 20})
        print(indicator.GetIndicatorValues())
        indicator.AdvanceTime(indicatorTimeSpan)


if __name__ == "__main__":
    TestTranscationBasedIndicators()
    TestBarBasedIndicators()