from GenIndicators import *
from datetime import datetime, timedelta
from indicators.BarChartIndicatorGen import *
from indicators.VWAPIndicatorGen import *
from indicators.SlidingVWAPIndicatorGen import *
from indicators.VolumeIndicatorGen import *
from indicators.MarketStructureIndicatorGen import *
from indicators.CVDIndicatorGen import *
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def GenerateAndPlot():
    filepath = ".\\minuteBarData\\testDelta.csv"

    indicatorTimeSpan = timedelta(minutes=15)

    indicators = []
    indicators.append(BarChartIndicatorGen(indicatorTimeSpan))
    # indicators.append(VWapIndicatorGen(indicatorTimeSpan))
    indicators.append(VolumeIndicatorGen(indicatorTimeSpan, VolumeType.Buy))
    indicators.append(VolumeIndicatorGen(indicatorTimeSpan, VolumeType.Sell))
    indicators.append(CVDIndicatorGen(indicatorTimeSpan))
    indicators.append(SlidingVWAPIndicatorGen(indicatorTimeSpan*24))


    # indicators.append(MarketStructureIndicatorGen(indicatorTimeSpan))

    GenerateIndicators(4, indicators, indicatorTimeSpan, filepath, True)

    df = pandas.read_csv(filepath)
    print(df.columns)

    annotations = []
    # #generate annotations and keep track of trend changes, continuations
    # trendChanges = pandas.Series(df['trend'].diff())
    # trends_filtered = trendChanges[trendChanges!=0]
    # trendConts = pandas.Series(df['cont'])
    # trendConts_filtered = trendConts[trendConts!=0]
    # moves = []
    # totalProfit = 1
    # totalProfitNoFees = 1

    # #add trend change annotations, keep track of trend changes
    # for index, change in trends_filtered.items():
    #    if change > 0:
    #        annotations.append(go.layout.Annotation(
    #            x=pandas.to_datetime(df.iloc[index].timestamp, format="%Y-%m-%dD%H:%M:%S"),
    #            y=df.iloc[index].close,
    #            showarrow=True,arrowhead=1,arrowcolor="green",arrowsize=2,arrowwidth=2,ax=0,ay=20))
    #        if len(moves)>0:
    #            totalProfitNoFees = totalProfitNoFees * (1+((moves[-1][1]-df.iloc[index].close)/moves[-1][1]))
    #            totalProfit = totalProfit * (1+((moves[-1][1]-df.iloc[index].close)/moves[-1][1])) * .99925
    #        moves.append([df.iloc[index].timestamp, df.iloc[index].close, 1, totalProfit, totalProfitNoFees])
    #    if change < 0:
    #        annotations.append(go.layout.Annotation(
    #            x=pandas.to_datetime(df.iloc[index].timestamp, format="%Y-%m-%dD%H:%M:%S"),
    #            y=df.iloc[index].close,
    #            showarrow=True,arrowhead=1,arrowcolor="red",arrowsize=2,arrowwidth=2,ax=0,ay=-20))
    #        if len(moves)>0:
    #            totalProfitNoFees = totalProfitNoFees * (1+((df.iloc[index].close-moves[-1][1])/moves[-1][1]))
    #            totalProfit = totalProfit * (1+((df.iloc[index].close-moves[-1][1])/moves[-1][1])) * .99925
    #        moves.append([df.iloc[index].timestamp, df.iloc[index].close, 0, totalProfit, totalProfitNoFees])
    # movesArray = numpy.array(moves)
    # print("num moves:", len(movesArray))
    # print("fees paid:", len(movesArray)*.0075)

    # #add trend continuation annotations
    # for index, change in trendConts_filtered.items():
    #     if change > 0:
    #         annotations.append(go.layout.Annotation(
    #            x=pandas.to_datetime(df.iloc[index].timestamp, format="%Y-%m-%dD%H:%M:%S"),
    #            y=df.iloc[index].close,
    #            showarrow=True,arrowhead=1,arrowcolor="green",arrowsize=1,arrowwidth=1,ax=0,ay=20))
    #     if change < 0:
    #         annotations.append(go.layout.Annotation(
    #            x=pandas.to_datetime(df.iloc[index].timestamp, format="%Y-%m-%dD%H:%M:%S"),
    #            y=df.iloc[index].close,
    #            showarrow=True,arrowhead=1,arrowcolor="red",arrowsize=1,arrowwidth=1,ax=0,ay=-20))

    start = pandas.to_datetime(df.iloc[0, 0], format="%Y-%m-%dD%H:%M:%S")
    end = pandas.to_datetime(df.iloc[-1, 0], format="%Y-%m-%dD%H:%M:%S")
    #init plotly and candlestick
    fig = make_subplots(rows=3, cols=1, row_heights=[0.8,0.2,0.2], vertical_spacing=0.01)
    fig.update_layout(dict(
        title='The Great Recession',
        yaxis_title='AAPL Stock',
        barmode='relative',
        annotations=annotations,
        xaxis=go.layout.XAxis(rangeslider=dict (visible = False))))
    fig.add_trace(go.Candlestick(
        x=pandas.to_datetime(df['timestamp'], format="%Y-%m-%dD%H:%M:%S"), 
        open=df['open'],
        high=df['high'],
        low=df['low'],
        close=df['close']))
    fig.update_xaxes(showgrid=False, showticklabels=False, row=1, col=1,
        range=[start, end])
    lower = df['low'].min()
    upper = df['high'].max()
    spread = upper - lower
    lower = lower - spread*.02
    upper = upper + spread*.02 
    fig.update_yaxes(row=1,col=1,range=[lower, upper])


    #plot vwaps
    fig.add_trace(go.Scatter(
        x=pandas.to_datetime(df['timestamp'], format="%Y-%m-%dD%H:%M:%S"),
        y=df['6hrSVWAP'], line=dict(color='rgb(0,0,256)', width=2)))

    # fig.add_trace(go.Scatter(
    #     x=pandas.to_datetime(df['timestamp'], format="%Y-%m-%dD%H:%M:%S"),
    #     y=df['vwap'], line=dict(color='rgb(0,0,0)', width=2)))

    # #plot highs and lows
    # fig.add_trace(go.Scatter(
    #    x=pandas.to_datetime(df['timestamp'], format="%Y-%m-%dD%H:%M:%S"),
    #    y=df['l1'], line=dict(color='rgb(255,100,100)', width=1)))
    # fig.add_trace(go.Scatter(
    #    x=pandas.to_datetime(df['timestamp'], format="%Y-%m-%dD%H:%M:%S"),
    #    y=df['h1'], line=dict(color='rgb(100,255,100)', width=1)))
    # fig.add_trace( go.Scatter(
    #    x=pandas.to_datetime(df['timestamp'], format="%Y-%m-%dD%H:%M:%S"),
    #    y=df['h2'], line=dict(color='rgb(0,255,0)', width=3)))
    # fig.add_trace(go.Scatter(
    #    x=pandas.to_datetime(df['timestamp'], format="%Y-%m-%dD%H:%M:%S"),
    #    y=df['l2'], line=dict(color='rgb(255,0,0)', width=3)))

    # #plot volume bars
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
    # fig.update_yaxes(title_text="Volume", showgrid=False, row=2, col=1)
    # fig.update_xaxes(showgrid=False, showticklabels=False, row=2, col=1, 
    # range=[start, end])

    #plot deviations
    fig.add_shape(type="line", x0=start, x1=end, y0=0, y1=0, line=dict(color="rgb(0,0,0)", width=1),row=2, col=1)
    fig.add_shape(type="rect", x0=start, x1=end, y0=1, y1=2, line=dict(color="rgb(255,0,0)", width=1),fillcolor='rgb(255,200,200)', row=2, col=1, layer='below')
    fig.add_shape(type="rect", x0=start, x1=end, y0=2, y1=3, line=dict(color="rgb(255,0,0)", width=1),fillcolor='rgb(255,100,100)', row=2, col=1, layer='below')
    fig.add_shape(type="rect", x0=start, x1=end, y0=-3, y1=-2, line=dict(color="rgb(0,255,0)", width=1), fillcolor='rgb(100,255,100)', row=2, col=1, layer='below')
    fig.add_shape(type="rect", x0=start, x1=end, y0=-2, y1=-1, line=dict(color="rgb(0,255,0)", width=1), fillcolor='rgb(200,255,200)', row=2, col=1, layer='below')
    fig.add_trace(go.Scatter(
        x=pandas.to_datetime(df['timestamp'], format="%Y-%m-%dD%H:%M:%S"),
        y=(df['close']-df['6hrSVWAP'])/df['6hrSVWAP_sigma'], line=dict(color='rgb(0,0,0)', width=1)),
        row=2, col=1)
    fig.update_yaxes(title_text="6hrSVWAP_devs", showgrid=False, row=2, col=1, range=[-3.5, 3.5])
    fig.update_xaxes(showgrid=False, showticklabels=False, row=2, col=1, 
        range=[start, end])

    fig.add_trace(go.Scatter(
        x=pandas.to_datetime(df['timestamp'], format="%Y-%m-%dD%H:%M:%S"),
        y=df['6hrSVWAP']+2*df['6hrSVWAP_sigma'], line=dict(color='rgb(160,0,0)', width=1)))
    fig.add_trace(go.Scatter(
        x=pandas.to_datetime(df['timestamp'], format="%Y-%m-%dD%H:%M:%S"),
        y=df['6hrSVWAP']+3*df['6hrSVWAP_sigma'], line=dict(color='rgb(160,0,0)', width=1), fill='tonexty'))
    fig.add_trace(go.Scatter(
        x=pandas.to_datetime(df['timestamp'], format="%Y-%m-%dD%H:%M:%S"),
        y=df['6hrSVWAP']-2*df['6hrSVWAP_sigma'], line=dict(color='rgb(0,160,0)', width=1)))
    fig.add_trace(go.Scatter(
        x=pandas.to_datetime(df['timestamp'], format="%Y-%m-%dD%H:%M:%S"),
        y=df['6hrSVWAP']-3*df['6hrSVWAP_sigma'], line=dict(color='rgb(0,160,0)', width=1), fill='tonexty'))

    #plot CVD
    fig.add_trace(go.Candlestick(
        x=pandas.to_datetime(df['timestamp'], format="%Y-%m-%dD%H:%M:%S"), 
        open=df['CVDo'],
        high=df['CVDh'],
        low=df['CVDl'],
        close=df['CVDc']), row=3, col=1)
    fig.update_yaxes(title_text="CVD", showgrid=False, row=3, col=1)
    fig.update_xaxes(showgrid=False, showticklabels=True, row=3, col=1, 
        range=[start, end], rangeslider=dict (visible = False))

    #plot delta
    # y = df['vdelta']
    # color = numpy.array(['rgb(255,255,255)']*y.shape[0])
    # color[y>0]='rgb(0,200,0)'
    # color[y<0]='rgb(200,0,0)'
    # fig.add_trace(go.Bar(
    #     x=pandas.to_datetime(df['timestamp'], format="%Y-%m-%dD%H:%M:%S"),
    #     y=y,
    #     marker=dict(color=color.tolist())),
    #     row=3, col=1) 
    # fig.update_yaxes(title_text=
    # "Volume Delta", showgrid=False, row=3, col=1)

    # #plot equity curve
    # if len(movesArray)>0:
    #     fig.add_trace(go.Scatter(
    #         x=pandas.to_datetime(movesArray[:,0], format="%Y-%m-%dD%H:%M:%S"),
    #         y=movesArray[:,3], line=dict(color='rgb(0,0,0)', width=2)), row=2, col=1)
    #     fig.add_trace(go.Scatter(
    #         x=pandas.to_datetime(movesArray[:,0], format="%Y-%m-%dD%H:%M:%S"),
    #         y=movesArray[:,4], line=dict(color='rgb(100,100,100)', width=2)), row=2, col=1)
    #     fig.update_yaxes(title_text="Percent profit", showgrid=False, row=2, col=1)
    
    fig.show()
    fig.write_html("delta_test.html")

if __name__ == "__main__":
    GenerateAndPlot()