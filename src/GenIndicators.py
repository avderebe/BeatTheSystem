import pandas
import numpy
import glob
import os
import pickle

from TransactionBasedIndicators.BarChartIndicatorGen import BarChartIndicatorGen
from TransactionBasedIndicators.VolumeIndicatorGen import *
from TransactionBasedIndicators.VWAPIndicatorGen import *
from BarBasedIndicators.SlidingVWAPIndicatorGen import SlidingVWAPIndicatorGen
from datetime import datetime, timedelta
from itertools import islice



def GenerateMinuteBars(nFiles, indicators, minuteBarTimeSpan, outputPath, regenerate=False, verbose = False):

    if minuteBarTimeSpan.microseconds != 0:
        raise Exception("Microseconds cannot be 0")

    if minuteBarTimeSpan.days != 0 and minuteBarTimeSpan.seconds != 0:
        raise Exception("time span must be either full days or fractions of a day")


    all_filenames = [a for a in glob.glob('.\\postProcessingData\\*.csv')]
    curTime = None
    lastFile = ""


    #regeneration or continue from last bar
    savedStatePath = os.path.join(os.path.dirname(outputPath), "savedState", os.path.basename(outputPath))

    #if neither important file exists, regenerate
    if not os.path.exists(outputPath) or not os.path.exists(savedStatePath):
        regenerate = True

    #Check if the indicators don't match the generated ones
    #If they don't match, the generated data will not be compatible, so regenerate
    if not regenerate:
        sampleRow = {'timestamp' : 0}
        for indicator in indicators:
            sampleRow.update(indicator.GetIndicatorValues())
        
        cols = pandas.read_csv(outputPath,nrows=1)
        if set(cols.columns.values) != set(sampleRow.keys()):
            regenerate = True

    #if this is true, we passed all the other checks
    #read the saved state into memory
    if not regenerate:
        savedState = None
        with open(savedStatePath, "rb") as f:
            savedState = pickle.load(f)

        for indicator in indicators:
            indicator.LoadState(savedState)

        curTime = savedState['timestamp']
        lastFile = savedState['lastFile']
        all_filenames = all_filenames[all_filenames.index(lastFile)+1:]

        #since we added an unclosed row to the end of the data file
        #and since we're loading the state for that bar
        #we are essentially recalculating the last bar
        #so delete the last bar, used the saved state and start from there
        df = pandas.read_csv(outputPath)
        df = df[:-1]
        df.to_csv(outputPath, index=False, header=True)


    if regenerate and os.path.exists(outputPath):
        os.remove(outputPath)

    #funky stuff for past data manipulation
    #Numpy Arrays and DataFrames are slow to append to, so use dict first
    data = []

    i = 0
    filesDone = 0

    for f in all_filenames:
        lastFile = f
        before = datetime.now()

        xbtData = pandas.read_csv(f)

        if curTime == None:
            #set up state with first transaction
            curTime = datetime.strptime(xbtData.loc[xbtData.index[0], 'timestamp'][:-3], "%Y-%m-%dD%H:%M:%S.%f")

            #need to round to nearest 5 min/10min/hr maybe?
            #doesn't round properly yet
            if minuteBarTimeSpan.days != 0:
                curTime = curTime.replace(hour=0,minute=0,second=0,microsecond=0)
            else:
                seconds = curTime.hour * 60 * 60 + curTime.minute * 60 + curTime.second
                curTime = curTime - timedelta(seconds = seconds % minuteBarTimeSpan.seconds,microseconds=curTime.microsecond)
            

        for idx, row in xbtData.iterrows():

            #parse out dateTime
            dt = datetime.strptime(row['timestamp'][:-3], "%Y-%m-%dD%H:%M:%S.%f")

            #This is to start/end a time period if enough time has passed
            #Advances times periods until the transaction falls within it
            while ((dt - curTime) >= minuteBarTimeSpan):
                newRow = {'timestamp' : curTime.strftime("%Y-%m-%dD%H:%M:%S")}
                for indicator in indicators:
                    #copy indicator vals from obj to the new row
                    ####### MULTIPLE INDICATORS OF SAME TIME WILL OVERWRITE EACHOTHER
                    ####### FIXED BY ADDING TIME PERIOD TO INDICATOR NAME
                    newRow.update(indicator.GetIndicatorValues())
                    indicator.AdvanceTime(minuteBarTimeSpan)
                data.append(newRow)
                i = i + 1
                #advance to next time period
                curTime = curTime + minuteBarTimeSpan

            #negative amount means sell volume
            #positive amount means buy volume
            amount = row['size'] * (1 if row['side'] == 'Buy' else -1)
            price = row['price']
            time = dt
            for indicator in indicators:
                indicator.ProcessTransation(time, amount, price)


        convData = pandas.DataFrame(data)

        if convData.size != 0:
            convData.to_csv(outputPath, mode="a", index=False, header=True if not os.path.exists(outputPath) else False)
            data.clear()
            del xbtData

        after = datetime.now()

        if verbose:
            print(f + " done. Time to process: " + str(after - before))

        filesDone = filesDone + 1
        if filesDone >= nFiles:
            break

        
    #after files are done, there's still one unclosed time period. Add that too
    newRow = {'timestamp' : curTime.strftime("%Y-%m-%dD%H:%M:%S")}
    for indicator in indicators:
        newRow.update(indicator.GetIndicatorValues())
    pandas.DataFrame([newRow]).to_csv(outputPath, mode="a", index=False, header=True if not os.path.exists(outputPath) else False)


    #save state of conversion
    saveState = {'timestamp' : curTime, 'lastFile' : lastFile}
    for indicator in indicators:
        saveState.update(indicator.GetState())

    if not os.path.exists(os.path.dirname(savedStatePath)):
        os.makedirs(os.path.dirname(savedStatePath))
    with open(savedStatePath, 'wb') as f:
        pickle.dump(saveState, f, pickle.HIGHEST_PROTOCOL)


def GenerateIndicators(indicators, filePath, outputPath, verbose = False):

    #funky stuff for past data manipulation
    #Numpy Arrays and DataFrames are slow to append to, so use dict first
    data = []
    prevTime = None

    if os.path.exists(outputPath):
        os.remove(outputPath)


    before = datetime.now()

    xbtData = pandas.read_csv(filePath)

    if prevTime == None:
        #set up state with first transaction
        prevTime = datetime.strptime(xbtData.loc[xbtData.index[0], 'timestamp'], "%Y-%m-%dD%H:%M:%S") 

    for idx, row in xbtData.iterrows():

        #parse out dateTime
        dt = datetime.strptime(row['timestamp'], "%Y-%m-%dD%H:%M:%S")
        delta = dt - prevTime

        newRow = {}
        newRow.update(row)
        for indicator in indicators:
            #its okay to preAdvance, since we want to get the bar data before the time period closes
            indicator.AdvanceTime(delta)
            indicator.ProcessBar(row)
            newRow.update(indicator.GetIndicatorValues())
        
        data.append(newRow)


    convData = pandas.DataFrame(data)

    if convData.size != 0:
        convData.to_csv(outputPath, mode="a", index=False, header=True)
        data.clear()
        del xbtData

    after = datetime.now()

    if verbose:
        print(outputPath + " done. Time to process: " + str(after - before))


def GenerateBuySellPredictors(filePath, outputPath, weightFunc, cutoffWeight = 0, buyColName = 'buyPredictor', sellColName = 'sellPredictor', verbose = False):
    if not os.path.exists(filePath):
        raise Exception("File does not exist")

    before = datetime.now()

    data = pandas.read_csv(filePath)

    #Generate buy/sell predictors based on full knowledge of past, present and future prices
    #Our optimal algorithm will be able to predict these values without knowledge of the future
    #So we generate the optimal moves, and train the Neural network to hopefully predict this
    #With incomplete data (since we don't know the future)
    buyPredictors = [0] * len(data)
    sellPredictors = [0] * len(data)
    for idx1, row1 in data.iterrows():
        for idx2, row2 in islice(data.iterrows(), idx1 + 1, None):
            weight = weightFunc(idx2 - idx1)
            if weight < cutoffWeight:
                break

            if row1['vwap'] < row2['vwap']:
                buyPredictors[idx1] = buyPredictors[idx1] + weight * (row2['vwap'] - row1['vwap']) / row1['vwap']
                sellPredictors[idx2] = sellPredictors[idx2] + weight * (row2['vwap'] - row1['vwap']) / row1['vwap'] 
            else:
                sellPredictors[idx1] = sellPredictors[idx1] + weight * (row1['vwap'] - row2['vwap']) / row1['vwap']
                buyPredictors[idx2] = buyPredictors[idx2] + weight * (row1['vwap'] - row2['vwap']) / row1['vwap']

        data.loc[idx1, buyColName] = buyPredictors[idx1]
        data.loc[idx1, sellColName] = sellPredictors[idx1]

    data.to_csv(outputPath, index=False, header=True)

    after = datetime.now()

    if verbose:
        print(outputPath + " done. Time to process: " + str(after - before))

if __name__ == "__main__":
    minuteBarTimeSpan = timedelta(hours = 2) #minutes

    #list of indicators that we will use to generate the data

    indicators = []
    indicators.append(BarChartIndicatorGen(minuteBarTimeSpan))
    indicators.append(VWapIndicatorGen(minuteBarTimeSpan)) #1day vwap
    indicators.append(VolumeIndicatorGen(minuteBarTimeSpan, VolumeType.Buy))
    indicators.append(VolumeIndicatorGen(minuteBarTimeSpan, VolumeType.Sell))
    indicators.append(VolumeIndicatorGen(minuteBarTimeSpan, VolumeType.All))

    GenerateMinuteBars(1, indicators, minuteBarTimeSpan, ".\\minuteBarData\\newData.csv", True, True)

    barIndicators = []
    barIndicators.append(SlidingVWAPIndicatorGen(timedelta(days=1)))
    GenerateIndicators(barIndicators, ".\\minuteBarData\\newData.csv", ".\\minuteBarData\\newDataF.csv", True)

    GenerateBuySellPredictors(".\\minuteBarData\\newDataF.csv", ".\\minuteBarData\\newDataPred.csv", lambda x : 1 / (10 + x), verbose=True)