import stockMarketAPI as sm

nvidiaData = sm.getApiIntraday('NVDA')
print(nvidiaData.head(4))

