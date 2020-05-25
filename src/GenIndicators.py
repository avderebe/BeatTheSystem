import pandas
import numpy
import glob
import os
import math
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from indicators.BarChartIndicatorGen import BarChartIndicatorGen
from indicators.VolumeIndicatorGen import *
from indicators.VWAPIndicatorGen import *
from datetime import datetime, timedelta

l3 = None

indicatorTimeSpan = timedelta(minutes=5) #minutes

#list of indicators that we will use to generate the data

indicators = []
indicators.append(BarChartIndicatorGen(indicatorTimeSpan))
indicators.append(VWapIndicatorGen(timedelta(days=7)))
indicators.append(VolumeIndicatorGen(indicatorTimeSpan, VolumeType.Buy))
indicators.append(VolumeIndicatorGen(indicatorTimeSpan, VolumeType.Sell))
indicators.append(VolumeIndicatorGen(indicatorTimeSpan, VolumeType.All))

#funky stuff for past data manipulation
#Numpy Arrays and DataFrames are slow to append to, so use dict first

data = {}



curTime = None


i = 0
all_filenames = [a for a in glob.glob('.\\postProcessingData\\*.csv')]
for f in all_filenames:


    xbtData = pandas.read_csv(f)

    if curTime == None:
        #set up state with first transaction
        curTime = datetime.strptime(xbtData.loc[xbtData.index[0], 'timestamp'][:-3], "%Y-%m-%dD%H:%M:%S.%f")

        #need to round to nearest 5 min/10min/hr maybe?
        #doesn't round properly yet
        curTime = curTime - timedelta(minutes=curTime.minute % round(indicatorTimeSpan.seconds / 60), seconds = curTime.second, microseconds=curTime.microsecond)

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
            data[i] = newRow
            i = i + 1
            print(newRow)

            df = pandas.DataFrame.from_dict(data)
            trendChanges = pandas.Series(df.loc['trend', : ].diff())
            trends_filtered = trendChanges[trendChanges!=0]

            print(l3)

            annotations = []
            moves = []
            totalProfit = 0

            for index, change in trends_filtered.items():
                if change > 0:
                    annotations.append(go.layout.Annotation(
                        x=pandas.to_datetime(df.loc['timestamp', index], format="%Y-%m-%dD%H:%M:%S"),
                        y=df.loc['close', index],
                        showarrow=True,arrowhead=1,arrowcolor="green",arrowsize=2,arrowwidth=2,ax=0,ay=20))
                    if len(moves)>1:
                        totalProfit += (moves[-1][1]-df.loc['close', index])/moves[-1][1]
                    moves.append([df.loc['timestamp', index], df.loc['close', index], 1, totalProfit])
                if change < 0:
                    annotations.append(go.layout.Annotation(
                        x=pandas.to_datetime(df.loc['timestamp', index], format="%Y-%m-%dD%H:%M:%S"),
                        y=df.loc['close', index],
                        showarrow=True,arrowhead=1,arrowcolor="red",arrowsize=2,arrowwidth=2,ax=0,ay=-20))
                    if len(moves)>1:
                        totalProfit += (df.loc['close', index]-moves[-1][1])/moves[-1][1]
                    moves.append([df.loc['timestamp', index], df.loc['close', index], 0, totalProfit])

            if i > 600: 
                movesArray = numpy.array(moves)
                print(moves)
                print(movesArray)
                fig = make_subplots(rows=2, cols=1, row_heights=[0.8,0.2])

                fig.add_trace(go.Candlestick(
                    x=pandas.to_datetime(df.loc['timestamp', : ], format="%Y-%m-%dD%H:%M:%S"), 
                    open=df.loc['open', : ],
                    high=df.loc['high', : ],
                    low=df.loc['low', : ],
                    close=df.loc['close', : ]))
                fig.add_trace(go.Scatter(
                    x=pandas.to_datetime(df.loc['timestamp', : ], format="%Y-%m-%dD%H:%M:%S"),
                    y=df.loc['l1', : ], line=dict(color='rgb(255,200,200)', width=1)))
                fig.add_trace( go.Scatter(
                    x=pandas.to_datetime(df.loc['timestamp', : ], format="%Y-%m-%dD%H:%M:%S"),
                    y=df.loc['h2', : ], line=dict(color='rgb(0,255,0)', width=2)))
                fig.add_trace(go.Scatter(
                    x=pandas.to_datetime(df.loc['timestamp', : ], format="%Y-%m-%dD%H:%M:%S"),
                    y=df.loc['l2', : ], line=dict(color='rgb(255,0,0)', width=1)))
                fig.add_trace(go.Scatter(
                    x=pandas.to_datetime(df.loc['timestamp', : ], format="%Y-%m-%dD%H:%M:%S"),
                    y=df.loc['h1', : ], line=dict(color='rgb(200,255,200)', width=2)))
                fig.add_trace(go.Scatter(
                    x=pandas.to_datetime(movesArray[:,0], format="%Y-%m-%dD%H:%M:%S"),
                    y=movesArray[:,3], line=dict(color='rgb(0,0,0)', width=2)), row=2, col=1)
                fig.update_layout(dict(
                    title='The Great Recession',
                    yaxis_title='AAPL Stock',
                    xaxis=go.layout.XAxis(rangeslider=dict (visible = False)),
                    annotations = annotations))
                fig.add_trace(go.Scatter(
                    x=pandas.to_datetime(df.loc['timestamp', : ], format="%Y-%m-%dD%H:%M:%S"),
                    y=df.loc['vwap', : ], line=dict(color='rgb(0,0,0)', width=2)))
                fig.update_yaxes(title_text="Percent profit", showgrid=False, row=2, col=1)
                fig.update_xaxes(range=[pandas.to_datetime(df.iloc[0, 0], format="%Y-%m-%dD%H:%M:%S"), pandas.to_datetime(df.iloc[0, -1], format="%Y-%m-%dD%H:%M:%S")], showgrid=False, row=2, col=1)
                fig.update_xaxes(range=[pandas.to_datetime(df.iloc[0, 0], format="%Y-%m-%dD%H:%M:%S"), pandas.to_datetime(df.iloc[0, -1], format="%Y-%m-%dD%H:%M:%S")], showgrid=False, row=1, col=1)

                fig.show()

            #advance to next time period
            curTime = curTime + indicatorTimeSpan

        #negative amount means sell volume
        #positive amount means buy volume
        amount = row['size'] * (1 if row['side'] == 'Buy' else -1)
        price = row['price']
        time = dt
        for indicator in indicators:
            indicator.ProcessTransation(time, amount, price)
