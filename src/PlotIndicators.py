from GenIndicators import *
from datetime import datetime, timedelta
from indicators.BarChartIndicatorGen import *
from indicators.VWAPIndicatorGen import *
from indicators.VolumeIndicatorGen import *

from indicators.MarketStructureIndicatorGen import *
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def GenerateAndPlot():
    filepath = ".\\minuteBarData\\test1237.csv"

    indicatorTimeSpan = timedelta(days=1)

    indicators = []
    indicators.append(BarChartIndicatorGen(indicatorTimeSpan))
    # indicators.append(VWapIndicatorGen(indicatorTimeSpan))
    # indicators.append(VolumeIndicatorGen(indicatorTimeSpan, VolumeType.Buy))
    # indicators.append(VolumeIndicatorGen(indicatorTimeSpan, VolumeType.Sell))
    indicators.append(MarketStructureIndicatorGen(indicatorTimeSpan))

    GenerateIndicators(1237, indicators, indicatorTimeSpan, filepath, True)

    df = pandas.read_csv(filepath)
    print(df.columns)
    #generate annotations and keep track of trend changes, continuations
    trendChanges = pandas.Series(df['trend'].diff())
    trends_filtered = trendChanges[trendChanges!=0]
    trendConts = pandas.Series(df['cont'])
    trendConts_filtered = trendConts[trendConts!=0]
    annotations = []
    moves = []
    totalProfit = 1
    totalProfitNoFees = 1

    #add trend change annotations, keep track of trend changes
    for index, change in trends_filtered.items():
       if change > 0:
           annotations.append(go.layout.Annotation(
               x=pandas.to_datetime(df.iloc[index].timestamp, format="%Y-%m-%dD%H:%M:%S"),
               y=df.iloc[index].close,
               showarrow=True,arrowhead=1,arrowcolor="green",arrowsize=2,arrowwidth=2,ax=0,ay=20))
           if len(moves)>0:
               totalProfitNoFees = totalProfitNoFees * (1+((moves[-1][1]-df.iloc[index].close)/moves[-1][1]))
               totalProfit = totalProfit * (1+((moves[-1][1]-df.iloc[index].close)/moves[-1][1])) * .99925
           moves.append([df.iloc[index].timestamp, df.iloc[index].close, 1, totalProfit, totalProfitNoFees])
       if change < 0:
           annotations.append(go.layout.Annotation(
               x=pandas.to_datetime(df.iloc[index].timestamp, format="%Y-%m-%dD%H:%M:%S"),
               y=df.iloc[index].close,
               showarrow=True,arrowhead=1,arrowcolor="red",arrowsize=2,arrowwidth=2,ax=0,ay=-20))
           if len(moves)>0:
               totalProfitNoFees = totalProfitNoFees * (1+((df.iloc[index].close-moves[-1][1])/moves[-1][1]))
               totalProfit = totalProfit * (1+((df.iloc[index].close-moves[-1][1])/moves[-1][1])) * .99925
           moves.append([df.iloc[index].timestamp, df.iloc[index].close, 0, totalProfit, totalProfitNoFees])
    movesArray = numpy.array(moves)

    #add trend continuation annotations
    for index, change in trendConts_filtered.items():
        if change > 0:
            annotations.append(go.layout.Annotation(
               x=pandas.to_datetime(df.iloc[index].timestamp, format="%Y-%m-%dD%H:%M:%S"),
               y=df.iloc[index].close,
               showarrow=True,arrowhead=1,arrowcolor="green",arrowsize=1,arrowwidth=1,ax=0,ay=20))
        if change < 0:
            annotations.append(go.layout.Annotation(
               x=pandas.to_datetime(df.iloc[index].timestamp, format="%Y-%m-%dD%H:%M:%S"),
               y=df.iloc[index].close,
               showarrow=True,arrowhead=1,arrowcolor="red",arrowsize=1,arrowwidth=1,ax=0,ay=-20))

    #init plotly and candlestick
    fig = make_subplots(rows=2, cols=1, row_heights=[0.9,0.2])
    fig.update_layout(dict(
        title='The Great Recession',
        yaxis_title='AAPL Stock',
        barmode='relative',
        annotations=annotations,
        xaxis=go.layout.XAxis(rangeslider=dict (visible = False))))
    fig.update_xaxes(range=[pandas.to_datetime(df.iloc[0, 0], format="%Y-%m-%dD%H:%M:%S"), pandas.to_datetime(df.iloc[-1, 0], format="%Y-%m-%dD%H:%M:%S")], showgrid=False, row=2, col=1)
    fig.update_xaxes(range=[pandas.to_datetime(df.iloc[0, 0], format="%Y-%m-%dD%H:%M:%S"), pandas.to_datetime(df.iloc[-1, 0], format="%Y-%m-%dD%H:%M:%S")], showgrid=False, row=1, col=1)
    fig.add_trace(go.Candlestick(
        x=pandas.to_datetime(df['timestamp'], format="%Y-%m-%dD%H:%M:%S"), 
        open=df['open'],
        high=df['high'],
        low=df['low'],
        close=df['close']))

    #plot highs and lows
    fig.add_trace(go.Scatter(
       x=pandas.to_datetime(df['timestamp'], format="%Y-%m-%dD%H:%M:%S"),
       y=df['l1'], line=dict(color='rgb(255,100,100)', width=1)))
    fig.add_trace(go.Scatter(
       x=pandas.to_datetime(df['timestamp'], format="%Y-%m-%dD%H:%M:%S"),
       y=df['h1'], line=dict(color='rgb(100,255,100)', width=1)))
    fig.add_trace( go.Scatter(
       x=pandas.to_datetime(df['timestamp'], format="%Y-%m-%dD%H:%M:%S"),
       y=df['h2'], line=dict(color='rgb(0,255,0)', width=3)))
    fig.add_trace(go.Scatter(
       x=pandas.to_datetime(df['timestamp'], format="%Y-%m-%dD%H:%M:%S"),
       y=df['l2'], line=dict(color='rgb(255,0,0)', width=3)))

    ##plot volume bars
    # fig.add_trace(go.Scatter(
    #     x=pandas.to_datetime(df['timestamp'], format="%Y-%m-%dD%H:%M:%S"),
    #     y=df['vwap'], line=dict(color='rgb(0,0,0)', width=2)))
    # fig.add_trace(go.Bar(
    #     x=pandas.to_datetime(df['timestamp'], format="%Y-%m-%dD%H:%M:%S"),
    #     y=df['vbuy'],
    #     marker=dict(color='rgb(0,200,0)')),
    #     row=2, col=1) 
    # fig.add_trace(go.Bar(
    #     x=pandas.to_datetime(df['timestamp'], format="%Y-%m-%dD%H:%M:%S"),
    #     y=df['vsell']*-1,
    #     marker=dict(color='rgb(200,0,0)')),
    #     row=2, col=1) 
    # fig.update_yaxes(title_text=
    # "Volume", showgrid=False, row=2, col=1)

    #plot equity curve
    if len(movesArray)>0:
        fig.add_trace(go.Scatter(
            x=pandas.to_datetime(movesArray[:,0], format="%Y-%m-%dD%H:%M:%S"),
            y=movesArray[:,3], line=dict(color='rgb(0,0,0)', width=2)), row=2, col=1)
        fig.add_trace(go.Scatter(
            x=pandas.to_datetime(movesArray[:,0], format="%Y-%m-%dD%H:%M:%S"),
            y=movesArray[:,4], line=dict(color='rgb(100,100,100)', width=2)), row=2, col=1)
        fig.update_yaxes(title_text="Percent profit", showgrid=False, row=2, col=1)
    
    fig.show()
    fig.write_html("7D1.html")
    print("num moves:", len(movesArray))
    print("fees paid:", len(movesArray)*.0075)
if __name__ == "__main__":
    GenerateAndPlot()