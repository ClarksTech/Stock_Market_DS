#-------------------------------------------- Import Required Modules --------------------------------------------#

import stockMarketAPI as sm
import stockIndicators as si
import stockVisualisors as sv
import os
import pandas as pd

#-------------------------------------------------- Main Script --------------------------------------------------#

# Prompt user to select stock for examination
stockTicker = input('Enter the ticker symbol for the stock you wish to examine, for example \'NVDA\': ')

# only perform the API call is th CSV does not exist to reduce calls to the API
dirPath = os.path.dirname(__file__)
filePath = f'{dirPath}\stockDataFiles\{stockTicker}.csv'

if(os.path.isfile(filePath)):
    print(f'Loading pre-existing data file for {stockTicker}...')
    stockData = pd.read_csv(filePath)
else:
    # Perform API call to get the stocks historical data
    print(f'Performing API call for {stockTicker}...')
    stockData = sm.getApiIntraday(stockTicker)

    # Generate all stock indicators adding to the dataframe
    print(f'Generating stock indicators for {stockTicker}...')
    stockData = si.genStockIndicators(stockData)
    print(f'Generating EMA signals for {stockTicker}...')
    stockData = stockData[-60000:]
    stockData.reset_index(inplace=True, drop=True)
    stockData = si.genEmaSignal(stockData)
    print(f'Generating total signals for {stockTicker}...')
    stockData = si.genTotalSignal(stockData)
    print(f'Generating RSI signals and updating total signal for {stockTicker}...')
    stockData = si.genRsiSignal(stockData)

    # save as csv file to prevent excess API calls and processing time in future program runs
    print(f'Saving data file for {stockTicker}...')
    stockData.to_csv(filePath, index=False)

# resize to smaller size for testing
print(stockData.shape[0])
print(stockData.totalSignal.value_counts())

# visualise the stock data
sv.plotStockData(stockData)


#------------------------------------------------ Main Script End -------------------------------------------------#

