from indicators.VolumeIndicatorGen import VolumeType,VolumeIndicatorGen
from indicators.BarChartIndicatorGen import BarChartIndicatorGen
from indicators.VWAPIndicatorGen import VWapIndicatorGen

def TestIndicators():
    indicators = []
    indicators.append(BarChartIndicatorGen(5))
    indicators.append(VolumeIndicatorGen(5, VolumeType.Buy))
    indicators.append(VolumeIndicatorGen(5, VolumeType.Sell))
    indicators.append(VolumeIndicatorGen(5, VolumeType.All))
    indicators.append(VWapIndicatorGen(5))

    for indicator in indicators:
        indicator.StartNewTimePeriod()
        indicator.ProcessTransation(0, 1, 10)
        indicator.ProcessTransation(0, 2, 20)
        indicator.ProcessTransation(0, -1, 5)
        indicator.ProcessTransation(0, -2, 45)
        indicator.ProcessTransation(0, 4, 15)

        print(indicator.GetIndicatorValues())

        indicator.StartNewTimePeriod()
        indicator.ProcessTransation(0, -2, 55)
        indicator.ProcessTransation(0, -1, 35)
        indicator.ProcessTransation(0, 3, 45)
        indicator.ProcessTransation(0, -2, 10)
        indicator.ProcessTransation(0, 5, 25)

        print(indicator.GetIndicatorValues())
        
        indicator.StartNewTimePeriod()
        indicator.ProcessTransation(0, 1, 35)
        indicator.ProcessTransation(0, 2, 75)
        indicator.ProcessTransation(0, 3, 65)
        indicator.ProcessTransation(0, 4, 85)
        indicator.ProcessTransation(0, 5, 70)

        print(indicator.GetIndicatorValues())


if __name__ == "__main__":
    TestIndicators()