import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime
import pandas as pd
import pandas_ta as ta

def pointPos(x):
    if x['totalSignal'] == 2:
        return x['low']-1e-4
    elif x['totalSignal']==1:
        return x['high']+1e-4
    else:
        return np.nan

def plotStockData(df: pd.DataFrame, bbLength=15, bbStd=1.5):
    """
    Plot the stock data displaying totalSignal points
    
    Parameter
    ---------
    df : pd.DataFrame
        data frame containing stock data
    bbLength : int, optional
        the number of candels to include in the bollinger bands moving average
    bbStd : int, optional
        the standard deviation level of the bollinger bands

    Returns
    ---------
    
    """
    df['pointPos'] = df.apply(lambda row: pointPos(row), axis=1)

    st=100
    dfpl = df[st:st+350]
    fig = go.Figure(data=[go.Candlestick(x=dfpl.index,
                    open=dfpl['open'],
                    high=dfpl['high'],
                    low=dfpl['low'],
                    close=dfpl['close']),
    
                    go.Scatter(x=dfpl.index, y=dfpl[f'BBL_{bbLength}_{bbStd}'],
                            line=dict(color='green', width=1),
                            name='BBL'),
                    go.Scatter(x=dfpl.index, y=dfpl[f'BBU_{bbLength}_{bbStd}'],
                            line=dict(color='green', width=1),
                            name='BBU'),
                    go.Scatter(x=dfpl.index, y=dfpl['emaFast'],
                            line=dict(color='black', width=1),
                            name='emaFast'),
                    go.Scatter(x=dfpl.index, y=dfpl['emaSlow'],
                            line=dict(color='blue', width=1),
                            name='emaSlow')])
    
    fig.add_scatter(x=dfpl.index, y=dfpl['pointPos'], mode='markers', marker=dict(size=8, color='MediumPurple'), name='entry')
    fig.update_layout(width=1200, height=800)
    fig.show()

    return()