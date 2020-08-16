from GenIndicators import *
from datetime import datetime, timedelta
from TransactionBasedIndicators.BarChartIndicatorGen import *
from TransactionBasedIndicators.VWAPIndicatorGen import *
from TransactionBasedIndicators.VolumeIndicatorGen import *
from BarBasedIndicators.SlidingVWAPIndicatorGen import *
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def GenerateAndPlot():
    filepath = ".\\minuteBarData\\test.csv"
    finalFilePath = ".\\minuteBarData\\testf.csv"
    predictiveMovePath = ".\\minuteBarData\\testp.csv"

    indicatorTimeSpan = timedelta(days=1)

    indicators = []
    indicators.append(BarChartIndicatorGen(indicatorTimeSpan))
    indicators.append(VWapIndicatorGen(indicatorTimeSpan))
    indicators.append(VolumeIndicatorGen(indicatorTimeSpan, VolumeType.Buy))
    indicators.append(VolumeIndicatorGen(indicatorTimeSpan, VolumeType.Sell))
    indicators.append(VolumeIndicatorGen(indicatorTimeSpan, VolumeType.All))

    #GenerateMinuteBars(30, indicators, indicatorTimeSpan, filepath, False, True)

    barIndicators = []
    barIndicators.append(SlidingVWAPIndicatorGen(indicatorTimeSpan * 7))

    GenerateIndicators(barIndicators, filepath, finalFilePath, True)


    #These weight functions basically assigns weight the effect of a price difference between two bars depending on their distance in time
    #short term, the weight shrinks by x^2
    #longer term x^1.75
    #long term x^1.5
    #Still WIP though, its hard to find a good weight
    #This will essentially be how we define the "optimal" move over the course of time
    #Given all the past/pres/future price movements, what is the "optimal" time to buy or sell
    #We will feed this into the neural network in hopes that it will learn to determine the "optimal"
    #moves by only feeding it the past/present data
    GenerateBuySellPredictors(finalFilePath, predictiveMovePath, lambda x : 1 / (8 + (x ** 2) / 6), 1/600, "shortTermBuy", "shortTermSell", verbose=True)
    GenerateBuySellPredictors(predictiveMovePath, predictiveMovePath, lambda x : 1 / (25 + (x ** 1.75) / 2), 1/4500, "longerTermBuy", "longerTermSell", verbose=True)
    GenerateBuySellPredictors(predictiveMovePath, predictiveMovePath, lambda x : 1 / (400 + (x ** 1.5)), 1/20124,  "longTermBuy", "longTermSell", verbose=True)

    df = pandas.read_csv(predictiveMovePath)

    #trendChanges = pandas.Series(df.loc['trend', : ].diff())
    #trends_filtered = trendChanges[trendChanges!=0]


    #annotations = []
    # moves = []
    #totalProfit = 0

    #
    #for index, change in trends_filtered.items():
    #    if change > 0:
    #        annotations.append(go.layout.Annotation(
    #            x=pandas.to_datetime(df.loc['timestamp', index], format="%Y-%m-%dD%H:%M:%S"),
    #            y=df.loc['close', index],
    #            showarrow=True,arrowhead=1,arrowcolor="green",arrowsize=2,arrowwidth=2,ax=0,ay=20))
    #        if len(moves)>1:
    #            totalProfit += (moves[-1][1]-df.loc['close', index])/moves[-1][1]
    #        moves.append([df.loc['timestamp', index], df.loc['close', index], 1, totalProfit])
    #    if change < 0:
    #        annotations.append(go.layout.Annotation(
    #            x=pandas.to_datetime(df.loc['timestamp', index], format="%Y-%m-%dD%H:%M:%S"),
    #            y=df.loc['close', index],
    #            showarrow=True,arrowhead=1,arrowcolor="red",arrowsize=2,arrowwidth=2,ax=0,ay=-20))
    #        if len(moves)>1:
    #            totalProfit += (df.loc['close', index]-moves[-1][1])/moves[-1][1]
    #        moves.append([df.loc['timestamp', index], df.loc['close', index], 0, totalProfit])


    #movesArray = numpy.array(moves)
    #print(moves)
    #print(movesArray)
    fig = make_subplots(rows=5, cols=1, row_heights=[0.8,0.2, 0.2,0.2,0.2], shared_xaxes=True)

    fig.add_trace(go.Candlestick(
        x=pandas.to_datetime(df['timestamp'], format="%Y-%m-%dD%H:%M:%S"), 
        open=df['open'],
        high=df['high'],
        low=df['low'],
        close=df['close']))
    #fig.add_trace(go.Scatter(
    #    x=pandas.to_datetime(df.loc['timestamp', : ], format="%Y-%m-%dD%H:%M:%S"),
    #    y=df.loc['l1', : ], line=dict(color='rgb(255,200,200)', width=1)))
    #fig.add_trace( go.Scatter(
    #    x=pandas.to_datetime(df.loc['timestamp', : ], format="%Y-%m-%dD%H:%M:%S"),
    #    y=df.loc['h2', : ], line=dict(color='rgb(0,255,0)', width=2)))
    #fig.add_trace(go.Scatter(
    #    x=pandas.to_datetime(df.loc['timestamp', : ], format="%Y-%m-%dD%H:%M:%S"),
    #    y=df.loc['l2', : ], line=dict(color='rgb(255,0,0)', width=1)))
    #fig.add_trace(go.Scatter(
    #    x=pandas.to_datetime(df.loc['timestamp', : ], format="%Y-%m-%dD%H:%M:%S"),
    #    y=df.loc['h1', : ], line=dict(color='rgb(200,255,200)', width=2)))
    #fig.add_trace(go.Scatter(
    #    x=pandas.to_datetime(movesArray[:,0], format="%Y-%m-%dD%H:%M:%S"),
    #    y=movesArray[:,3], line=dict(color='rgb(0,0,0)', width=2)), row=2, col=1)
    fig.update_layout(dict(
        title='The Great Recession',
        yaxis_title='AAPL Stock',
        barmode='relative',
        xaxis=go.layout.XAxis(rangeslider=dict (visible = False))))
    fig.add_trace(go.Scatter(
        x=pandas.to_datetime(df['timestamp'], format="%Y-%m-%dD%H:%M:%S"),
        y=df['vwap'], line=dict(color='rgb(256,0,0)', width=2)))
    fig.add_trace(go.Scatter(
        x=pandas.to_datetime(df['timestamp'], format="%Y-%m-%dD%H:%M:%S"),
        y=df['7daySVWAP'], line=dict(color='rgb(0,0,256)', width=2)))
    fig.update_yaxes(title_text="Percent profit", showgrid=False, row=2, col=1)
    fig.add_trace(go.Bar(
        x=pandas.to_datetime(df['timestamp'], format="%Y-%m-%dD%H:%M:%S"),
        y=df['vbuy'],
        marker=dict(color='rgb(0,200,0)')),
        row=2, col=1) 
    fig.add_trace(go.Bar(
        x=pandas.to_datetime(df['timestamp'], format="%Y-%m-%dD%H:%M:%S"),
        y=df['vsell']*-1,
        marker=dict(color='rgb(200,0,0)')),
        row=2, col=1)
    fig.add_trace(go.Scatter(
        x=pandas.to_datetime(df['timestamp'], format="%Y-%m-%dD%H:%M:%S"),
        y=df['shortTermBuy'], line=dict(color='rgb(0,200,0)', width=2)),
        row=3, col=1)
    fig.add_trace(go.Scatter(
        x=pandas.to_datetime(df['timestamp'], format="%Y-%m-%dD%H:%M:%S"),
        y=df['longerTermBuy'], line=dict(color='rgb(0,150,0)', width=2)),
        row=4, col=1)
    fig.add_trace(go.Scatter(
        x=pandas.to_datetime(df['timestamp'], format="%Y-%m-%dD%H:%M:%S"),
        y=df['longTermBuy'], line=dict(color='rgb(0,100,0)', width=2)),
        row=5, col=1)
    fig.add_trace(go.Scatter(
        x=pandas.to_datetime(df['timestamp'], format="%Y-%m-%dD%H:%M:%S"),
        y=df['shortTermSell'], line=dict(color='rgb(200,0,0)', width=2)),
        row=3, col=1)
    fig.add_trace(go.Scatter(
        x=pandas.to_datetime(df['timestamp'], format="%Y-%m-%dD%H:%M:%S"),
        y=df['longerTermSell'], line=dict(color='rgb(150,0,0)', width=2)),
        row=4, col=1) 
    fig.add_trace(go.Scatter(
        x=pandas.to_datetime(df['timestamp'], format="%Y-%m-%dD%H:%M:%S"),
        y=df['longTermSell'], line=dict(color='rgb(100,0,0)', width=2)),
        row=5, col=1)  

    fig.update_yaxes(title_text="Volume", showgrid=False, row=2, col=1)
    fig.update_xaxes(range=[pandas.to_datetime(df.iloc[0, 0], format="%Y-%m-%dD%H:%M:%S"), pandas.to_datetime(df.iloc[-1, 0], format="%Y-%m-%dD%H:%M:%S")], showgrid=False, row=3, col=1)
    fig.update_xaxes(range=[pandas.to_datetime(df.iloc[0, 0], format="%Y-%m-%dD%H:%M:%S"), pandas.to_datetime(df.iloc[-1, 0], format="%Y-%m-%dD%H:%M:%S")], showgrid=False, row=2, col=1)
    fig.update_xaxes(range=[pandas.to_datetime(df.iloc[0, 0], format="%Y-%m-%dD%H:%M:%S"), pandas.to_datetime(df.iloc[-1, 0], format="%Y-%m-%dD%H:%M:%S")], showgrid=False, row=1, col=1)

    fig.update_xaxes(matches="x")
    fig.show()


if __name__ == "__main__":
    GenerateAndPlot()