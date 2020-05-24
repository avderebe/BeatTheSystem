from indicators.VolumeIndicatorGen import VolumeType,VolumeIndicatorGen
from indicators.BarChartIndicatorGen import BarChartIndicatorGen
from indicators.VWAPIndicatorGen import VWapIndicatorGen
from datetime import timedelta

def TestIndicators():
    indicatorTimeSpan = timedelta(minutes=5)
    indicators = []
    indicators.append(BarChartIndicatorGen(indicatorTimeSpan))
    indicators.append(VolumeIndicatorGen(indicatorTimeSpan, VolumeType.Buy))
    indicators.append(VolumeIndicatorGen(indicatorTimeSpan, VolumeType.Sell))
    indicators.append(VolumeIndicatorGen(indicatorTimeSpan, VolumeType.All))
    indicators.append(VWapIndicatorGen(indicatorTimeSpan))
    indicators.append(VWapIndicatorGen(indicatorTimeSpan*3))

    for indicator in indicators:
        indicator.ProcessTransation(0, 1, 1)
        indicator.ProcessTransation(0, 2, 20)
        indicator.ProcessTransation(0, -1, 5)
        indicator.ProcessTransation(0, -2, 45)
        indicator.ProcessTransation(0, 4, 15)

        print(indicator.GetIndicatorValues())
        indicator.AdvanceTime(indicatorTimeSpan)


if __name__ == "__main__":
    TestIndicators()