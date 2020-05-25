from GenIndicators import *
from datetime import datetime, timedelta
from indicators.BarChartIndicatorGen import *
from indicators.VWAPIndicatorGen import *
    df = pandas.read_csv(filepath)

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
    fig = make_subplots(rows=2, cols=1, row_heights=[0.8,0.2])

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
        xaxis=go.layout.XAxis(rangeslider=dict (visible = False))))
    fig.add_trace(go.Scatter(
        x=pandas.to_datetime(df['timestamp'], format="%Y-%m-%dD%H:%M:%S"),
        y=df['vwap'], line=dict(color='rgb(0,0,0)', width=2)))
    fig.update_yaxes(title_text="Percent profit", showgrid=False, row=2, col=1)
    fig.update_xaxes(range=[pandas.to_datetime(df.iloc[0, 0], format="%Y-%m-%dD%H:%M:%S"), pandas.to_datetime(df.iloc[-1, 0], format="%Y-%m-%dD%H:%M:%S")], showgrid=False, row=2, col=1)
    fig.update_xaxes(range=[pandas.to_datetime(df.iloc[0, 0], format="%Y-%m-%dD%H:%M:%S"), pandas.to_datetime(df.iloc[-1, 0], format="%Y-%m-%dD%H:%M:%S")], showgrid=False, row=1, col=1)

    fig.show()


if __name__ == "__main__":
    GenerateAndPlot()