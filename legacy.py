import pandas as pd
import yfinance as yf
import plotly.io as pio
import plotly.graph_objects as go
pio.templates.default = "plotly_white"

# Define the Stock tickers
nvidiaTicker = "NVDA"
metaTicker = "META"

# Define time period of data
startDate = "2023-01-01"
endDate = "2024-01-01"

# Fetch the historical stock data
nvidiaData = yf.download(nvidiaTicker, start=startDate, end=endDate)
metaData = yf.download(metaTicker, start=startDate, end=endDate)

# Create daily returns
nvidiaData['dailyReturn'] = nvidiaData['Adj Close'].pct_change()
metaData['dailyReturn'] = metaData['Adj Close'].pct_change()

# Visualise the daily returns
fig = go.Figure()
fig.add_trace(go.Scatter(x=nvidiaData.index, y=nvidiaData['dailyReturn'],
                         mode='lines', name='NVIDIA', line=dict(color='green')))
fig.add_trace(go.Scatter(x=metaData.index, y=metaData['dailyReturn'],
                         mode='lines', name='META', line=dict(color='blue')))
fig.update_layout(title='Daily Returns for NVIDIA and META (2023)',
xaxis_title='Date', yaxis_title='Daily Return',
legend=dict(x=0.02, y=0.95))
fig.show()

# Calculate cumulative returns over the quater
nvidiaCumulative = (1 + nvidiaData['dailyReturn']).cumprod() - 1
metaCumulative = (1 + metaData['dailyReturn']).cumprod() -1

# Visualise the cumulative returns
fig = go.Figure()
fig.add_trace(go.Scatter(x=nvidiaCumulative.index, y=nvidiaCumulative,
                         mode='lines', name='NVIDIA', line=dict(color='green')))
fig.add_trace(go.Scatter(x=metaCumulative.index, y=metaCumulative,
                         mode='lines', name='META', line=dict(color='blue')))
fig.update_layout(title='Cumulative Returns for NVIDIA and META (2023)',
xaxis_title='Date', yaxis_title='Cumulative Return',
legend=dict(x=0.02, y=0.95))
fig.show()

# Calculate volatility (stdd daily return)
nvidiaVolatility = nvidiaData['dailyReturn'].std()
metaVolatility = metaData['dailyReturn'].std()

# Visualise volatility
fig1 = go.Figure()
fig1.add_bar(x=['NVIDIA', 'META'], y=[nvidiaVolatility, metaVolatility],
             text=[f'{nvidiaVolatility:.4f}', f'{metaVolatility:.4f}'],
             textposition='auto', marker=dict(color=['green', 'blue']))

fig1.update_layout(title='Volatility Comparison (2023)',
                   xaxis_title='Stock', yaxis_title='Volatility',
                   bargap=0.5)
fig1.show()

# Compare to S&P500 (the market)
marketData = yf.download('^GSPC', start=startDate, end=endDate)
marketData['dailyReturn'] = marketData['Adj Close'].pct_change()

# Calculate Beta for NVIDIA and META
covNvidia = nvidiaData['dailyReturn'].cov(marketData['dailyReturn'])
varMarket = marketData['dailyReturn'].var()

betaNvidia = covNvidia / varMarket

covMeta = metaData['dailyReturn'].cov(marketData['dailyReturn'])

betaMETA = covMeta / varMarket

# Compare Beta values
if betaNvidia > betaMETA:
    conclusion = "NVIDIA is more volatiole (higher Beta) compared to META."
else:
    conclusion = "META is more volatile (higher Beta) compared to NVIDIA."

# Print the conclusion
print("Beta for NVIDIA:", betaNvidia)
print("Beta for META", betaMETA)
print(conclusion)

