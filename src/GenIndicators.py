import pandas
import numpy

from indicators.BarChartIndicatorGen import BarChartIndicatorGen
from indicators.VolumeIndicatorGen import *
from indicators.VWAPIndicatorGen import *
from datetime import datetime, timedelta


indicatorTimeSpan = 1 #minutes

#list of indicators that we will use to generate the data
indicators = []
indicators.append(BarChartIndicatorGen(indicatorTimeSpan))
indicators.append(VWapIndicatorGen(indicatorTimeSpan))
indicators.append(VolumeIndicatorGen(indicatorTimeSpan, VolumeType.Buy))
indicators.append(VolumeIndicatorGen(indicatorTimeSpan, VolumeType.Sell))
indicators.append(VolumeIndicatorGen(indicatorTimeSpan, VolumeType.All))

#funky stuff for past data manipulation
#Numpy Arrays and DataFrames are slow to append to, so use dict first

data = {}

xbtData = pandas.read_csv(".\postProcessingData\XBT20170101.csv")

#set up state with first transaction
curTime = datetime.strptime(xbtData.loc[xbtData.index[0], 'timestamp'][:-3], "%Y-%m-%dD%H:%M:%S.%f")
curTime = curTime - timedelta(minutes=curTime.minute % indicatorTimeSpan, seconds = curTime.second, microseconds=curTime.microsecond)
for indicator in indicators:
    indicator.StartNewTimePeriod()

i = 0

for idx, row in xbtData.iterrows():

    #parse out dateTime
    dt = datetime.strptime(row['timestamp'][:-3], "%Y-%m-%dD%H:%M:%S.%f")

    #This is to start/end a time period if enough time has passed
    #Advances times periods until the transaction falls within it
    while ((dt - curTime).seconds / 60 >= indicatorTimeSpan):
        newRow = {'timestamp' : curTime.strftime("%Y-%m-%dD%H:%M:%S")}
        for indicator in indicators:
            #copy indicator vals from obj to the new row
            newRow.update(indicator.GetIndicatorValues())
            indicator.StartNewTimePeriod()
        print(newRow)
        data[i] = newRow

        #advance to next time period
        curTime = curTime + timedelta(minutes = indicatorTimeSpan)

    #negative amount means sell volume
    #positive amount means buy volume
    amount = row['size'] * (1 if row['side'] == 'Buy' else -1)
    price = row['price']
    time = dt
    for indicator in indicators:
        indicator.ProcessTransation(time, amount, price)
