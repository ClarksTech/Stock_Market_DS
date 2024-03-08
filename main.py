#-------------------------------------------- Import Required Modules --------------------------------------------#

import stockMarketAPI as sm
import stockIndicators as si
import stockVisualisors as sv
import os
import pandas as pd

#-------------------------------------------------- Main Script --------------------------------------------------#

# Prompt user to select stock for examination
stockTicker = input('Enter the ticker symbol for the stock you wish to examine, for example \'NVDA\':')

# only perform the API call is th CSV does not exist to reduce calls to the API
path = f'/stockDataFiles/{stockTicker}.csv'

if(os.path.isfile(path)):
    df = pd.read_csv(f'/stockDataFiles/{stockTicker}.csv')
else:
    # Perform API call to get the stocks historical data
    stockData = sm.getApiIntraday(stockTicker)
    print(stockData.head(1))
    print(stockData.tail(1))
    stockData = stockData.iloc[-500:]
    print(stockData.head(1))
    print(stockData.tail(1))
    print(stockData.shape[0])

    # Generate all stock indicators adding to the dataframe
    stockData = si.genStockIndicators(stockData)
    stockData = si.genEmaSignal(stockData)
    stockData = si.genTotalSignal(stockData)
    stockData = si.genRsiSignal(stockData)
    sv.plotStockData(stockData)
    print(stockData.head(50))
    print(stockData.totalSignal.value_counts())

    # save as csv file to prevent excess API calls and processing time in future program runs
    stockData.to_csv(f'/stockDataFiles/{stockTicker}.csv', index=False)

#------------------------------------------------ Main Script End -------------------------------------------------#

