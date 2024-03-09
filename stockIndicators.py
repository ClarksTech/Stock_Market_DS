import pandas as pd
import pandas_ta as ta
import numpy as np

def genStockIndicators(df: pd.DataFrame, emaSlowLength=50, emaFastLength=30, rsiLength=10, bbLength=15, bbStd=1.5, atrLength=7) -> pd.DataFrame:
    """
    Return a dataframe containing specified stock historical data and movement indicators
    
    Parameter
    ---------
    df : pd.DataFrame
        data frame containing stock data
    emaSlowLength : int, optional
        the number of candels to include in the slow moving average
    emaFastLength : int, optional
        the number of candels to include in the fast moving average
    rsiLength : int, optional
        the number of candels to include in the relative strength index
    bbLength : int, optional
        the number of candels to include in the bollinger bands moving average
    bbStd : int, optional
        the standard deviation level of the bollinger bands
    atrLength : int, optional
        the number of candels to include in the average true range

    Returns
    ---------
    df : pandas DataFrame
        dataframe containing the specific stock historical timeseries data with following indicators added:
            - emaSlow
            - emaFast
            - rsi
            - atr
            - bb
    """
    df['emaSlow']=ta.ema(df.close, emaSlowLength)
    df['emaFast']=ta.ema(df.close, emaFastLength)
    df['rsi']=ta.ema(df.close, rsiLength)
    df['atr']=ta.atr(df.high, df.low, df.close, atrLength)
    bb = ta.bbands(df.close, bbLength, bbStd)
    df=df.join(bb)

    return(df)

def genEmaSignal(df: pd.DataFrame, backCandelsLength=7) -> pd.DataFrame:
    """
    Return a dataframe containing specified stock historical data and signal indicators based on ema
    
    Parameter
    ---------
    df : pd.DataFrame
        data frame containing stock data
    backCandelsLength : int, optional
        the number of candels to include in the rolling window

    Returns
    ---------
    df : pandas DataFrame
        dataframe containing the specific stock historical timeseries data with emaSignal added:
            - emaSignal = 0 : No Signal
            - emaSignal = 1 : Down trend
            - emaSignal = 2 : Up trend
    """
    
    # boolean series for conditions:
    above = df['emaFast'] > df['emaSlow']
    below = df['emaSlow'] > df['emaFast']

    # moving window verifying if all backcandels are meeting condition
    allAbove = above.rolling(window=backCandelsLength).apply(lambda x: x.all(), raw=True).fillna(0).astype(bool)
    allBelow = below.rolling(window=backCandelsLength).apply(lambda x: x.all(), raw=True).fillna(0).astype(bool)

    # assign identified signal
    df['emaSignal'] = 0
    df.loc[allBelow, 'emaSignal'] = 1
    df.loc[allAbove, 'emaSignal'] = 2

    return(df)

def genTotalSignal(df: pd.DataFrame, bbLength=15, bbStd=1.5) -> pd.DataFrame:
    """
    Return a dataframe containing specified stock historical data and buy / sell signal
    
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
    df : pandas DataFrame
        dataframe containing the specific stock historical timeseries data with totalSignal added:
            - totalSignal = 0 : No Signal
            - totalSignal = 1 : Sell
            - totalSignal = 2 : Buy
    """
    
    # vectorised conditions:
    condBuy = (df['emaSignal'] == 2) & (df['close'] <= df[f'BBL_{bbLength}_{bbStd}'])
    condSell = (df['emaSignal'] == 1) & (df['close'] >= df[f'BBU_{bbLength}_{bbStd}'])

    # assign identified signal
    df['totalSignal'] = 0
    df.loc[condSell, 'totalSignal'] = 1
    df.loc[condBuy, 'totalSignal'] = 2

    return(df)

def genRsiSignal(df: pd.DataFrame, rsiLength=5, rsiUpLimit=50.1, rsiDownLimit=49.9) -> pd.DataFrame:
    """
    Return a dataframe containing specified stock historical data and rsi signal
    updating the buy / sell signal to include this indicator
    
    Parameter
    ---------
    df : pd.DataFrame
        data frame containing stock data
    rsiLength : int, optional
        the number of candels to include in the rsi moving average
    rsiUpLimit : int, optional
        the up trend rsi limit
    rsiDownLimit : int, optional
        the down trend rsi limit 

    Returns
    ---------
    df : pandas DataFrame
        dataframe containing the specific stock historical timeseries data with rsiSignal added:
            - totalSignal = 0 : No Signal
            - totalSignal = 1 : Down trend
            - totalSignal = 2 : Up trend
        
        The total buy / sell signal is also updated to include this metric
    """
    
    rsiSignal = np.zeros(len(df['rsi']))
    for i in range(len(df['rsi'])):
        windowStart = max(0, i-rsiLength)
        window = df['rsi'][windowStart:i]
        if not window.empty and window.gt(rsiUpLimit).all():
            rsiSignal[i] = 2
        elif not window.empty and window.lt(rsiDownLimit).all():
            rsiSignal[i] = 1

    df['rsiSignal'] = rsiSignal
    df['totalSignal'] = df.apply(lambda row: row['totalSignal'] if row['totalSignal'] == row['rsiSignal'] else 0, axis=1)

    return(df)


