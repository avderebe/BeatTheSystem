import pandas
import numpy
import glob
import os

from indicators.BarChartIndicatorGen import BarChartIndicatorGen
from indicators.VolumeIndicatorGen import *
from indicators.VWAPIndicatorGen import *
from datetime import datetime, timedelta

def GenerateIndicators(nFiles, indicators, indicatorTimeSpan, outputPath, verbose = False):
    #funky stuff for past data manipulation
    #Numpy Arrays and DataFrames are slow to append to, so use dict first
    data = []
    curTime = None
    i = 0
    filesDone = 0

    if os.path.exists(outputPath):
        os.remove(outputPath)

    all_filenames = [a for a in glob.glob('.\\postProcessingData\\*.csv')]
    for f in all_filenames:

        before = datetime.now()

        xbtData = pandas.read_csv(f)

        if curTime == None:
            #set up state with first transaction
            curTime = datetime.strptime(xbtData.loc[xbtData.index[0], 'timestamp'][:-3], "%Y-%m-%dD%H:%M:%S.%f")

            #need to round to nearest 5 min/10min/hr maybe?
            #doesn't round properly yet
            curTime = curTime - timedelta(minutes=curTime.minute % round(indicatorTimeSpan.seconds / 60), seconds = curTime.second, microseconds=curTime.microsecond)
            # curTime = curTime - timedelta(minutes=curTime.minute, seconds = curTime.second, microseconds=curTime.microsecond)

        for idx, row in xbtData.iterrows():

            #parse out dateTime
            dt = datetime.strptime(row['timestamp'][:-3], "%Y-%m-%dD%H:%M:%S.%f")

            #This is to start/end a time period if enough time has passed
            #Advances times periods until the transaction falls within it
            while ((dt - curTime) >= indicatorTimeSpan):
                newRow = {'timestamp' : curTime.strftime("%Y-%m-%dD%H:%M:%S")}
                for indicator in indicators:
                    #copy indicator vals from obj to the new row
                    ####### MULTIPLE INDICATORS OF SAME TIME WILL OVERWRITE EACHOTHER
                    ####### MUST BE FIXED
                    newRow.update(indicator.GetIndicatorValues())
                    indicator.AdvanceTime(indicatorTimeSpan)
                data.append(newRow)
                i = i + 1
                #advance to next time period
                curTime = curTime + indicatorTimeSpan

            #negative amount means sell volume
            #positive amount means buy volume
            amount = row['size'] * (1 if row['side'] == 'Buy' else -1)
            price = row['price']
            time = dt
            for indicator in indicators:
                indicator.ProcessTransation(time, amount, price)


        convData = pandas.DataFrame(data)

        header = True
        if os.path.exists(outputPath):
            header = False
        convData.to_csv(outputPath, mode="a", index=False, header=header)
        
        data.clear()
        del xbtData

        after = datetime.now()

        if verbose:
            print(f + " done. Time to process: " + str(after - before))

        filesDone = filesDone + 1
        if filesDone >= nFiles:
            break


if __name__ == "__main__":
    indicatorTimeSpan = timedelta(minutes=5) #minutes

    #list of indicators that we will use to generate the data

    indicators = []
    indicators.append(BarChartIndicatorGen(indicatorTimeSpan))
    indicators.append(VWapIndicatorGen(timedelta(days=1))) #1day vwap
    indicators.append(VolumeIndicatorGen(indicatorTimeSpan, VolumeType.Buy))
    indicators.append(VolumeIndicatorGen(indicatorTimeSpan, VolumeType.Sell))
    indicators.append(VolumeIndicatorGen(indicatorTimeSpan, VolumeType.All))

    GenerateIndicators(5, indicators, indicatorTimeSpan, ".\\minuteBarData\\newData.csv", True)