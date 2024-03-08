from dotenv import load_dotenv
import os
import requests
import pandas as pd
import pandas_ta as ta

load_dotenv()

apiKey = os.getenv("ALPHA_VANTAGE_API_KEY")

def getApiIntraday(symbol: str, function='TIME_SERIES_INTRADAY', interval='1min', month='', outputsize='full') -> pd.DataFrame:
    """
    Return a dataframe containing specified stock historical data
    
    Parameter
    ---------
    symbol : str
        the ticker symbol of the desired stock
    function : str, optional
        the api temporal resolution (default intraday)
    interval : str, optional
        the time interval between consecutive data points in the intraday time series (default 1 min)
    month : str, optional
        the specific month to provide data for when intraday time series selected (default empty = past 30 days)
    outputsize : str, optional
        the size of data requested from the API

    Returns
    ---------
    df : pandas DataFrame
        dataframe containing the specific stock historical timeseries data
    
    References
    ---------
    ..[1] https://www.alphavantage.co/documentation/

    """
    
    # Alter the API call depending on the time series selected, as selection invalidates certain parameters
    if(function == 'TIME_SERIES_INTRADAY'):
        apiUrl = f'https://www.alphavantage.co/query?function={function}&symbol={symbol}&interval={interval}&month={month}&outputsize={outputsize}&datatype=csv&apikey=apiKey'
    elif (function == 'TIME_SERIES_DAILY'):
        apiUrl = f'https://www.alphavantage.co/query?function={function}&symbol={symbol}&outputsize={outputsize}&datatype=csv&apikey=apiKey'
    else:
        raise Exception("API function error, please check arguments and try again!")

    df = pd.read_csv(apiUrl)
    df = pd.DataFrame(df)

    # remove days where no movement i.e. weekends
    df=df[df.high!=df.low]
    df.set_index('timestamp', inplace=True)

    # save as csv file to prevent excess api call
    df.to_csv(f'/stockDataFiles/{symbol}.csv', index=False)

    return(df)





