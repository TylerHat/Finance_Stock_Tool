import pandas as pd
import numpy as np
import yfinance as yf
import plotly.graph_objs as go
import plotly.io as pio
import webview

def testing():
    print("helloWorld")

# Define a function to create and get the Bollinger Bands
def bollinger_bands(data, window_size=30):
    rolling_mean = data['Close'].rolling(window=window_size).mean()  # Simple Moving Average (SMA)
    rolling_std = data['Close'].rolling(window=window_size).std()
    data['UpperBand'] = rolling_mean + (2 * rolling_std)
    data['LowerBand'] = rolling_mean - (2 * rolling_std)
    return data

# Define a function to create and get the Relative Strength Index (RSI)
def rsi(data, window=14):
    delta = data['Close'].diff()
    gain = delta.where(delta > 0, 0)
    loss = delta.where(delta < 0, 0)
    avg_gain = gain.rolling(window).mean()
    avg_loss = loss.abs().rolling(window).mean()
    RS = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + RS))
    data['RSI'] = rsi
    data['Overbought'] = 70
    data['Oversold'] = 30
    return data

# Create and get the trading strategy
def strategy(data):
    position = 0  # shares
    buy_price = []
    sell_price = []
    for i in range(len(data)):
        if data['Close'][i] < data['LowerBand'][i] and data['RSI'][i] < data['Oversold'][i] and position == 0:
            position = 1
            buy_price.append(data['Close'][i])
            sell_price.append(np.nan)
        elif data['Close'][i] > data['UpperBand'][i] and data['RSI'][i] > data['Overbought'][i] and position == 1:
            position = 0
            sell_price.append(data['Close'][i])
            buy_price.append(np.nan)
        else:
            buy_price.append(np.nan)
            sell_price.append(np.nan)
    return buy_price, sell_price

# Get stock data
def get_stock_data(ticker: str, days: int) -> pd.DataFrame:
    end_date = pd.to_datetime('today')
    start_date = end_date - pd.Timedelta(days=days)
    stock_data = yf.download(ticker, start=start_date, end=end_date)
    return stock_data

def bollingBandsRSI_test(ticker, days):
    data = get_stock_data(ticker, days)
    data = bollinger_bands(data)
    data = rsi(data)
    buy_price, sell_price = strategy(data)
    data['Buy'] = buy_price
    data['Sell'] = sell_price

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data.index, y=data['Close'], mode='lines', name='Closing Price', line=dict(color='blue', width=2)))
    fig.add_trace(go.Scatter(x=data.index, y=data['UpperBand'], mode='lines', name='Upper Band', line=dict(color='yellow', width=1)))
    fig.add_trace(go.Scatter(x=data.index, y=data['LowerBand'], mode='lines', name='Lower Band', line=dict(color='purple', width=1)))
    fig.add_trace(go.Scatter(x=data.index, y=data['Buy'], mode='markers', name='Buy', marker=dict(color='green', symbol='triangle-up', size=10)))
    fig.add_trace(go.Scatter(x=data.index, y=data['Sell'], mode='markers', name='Sell', marker=dict(color='red', symbol='triangle-down', size=10)))

    fig.update_layout(
        title=f'Bollinger Bands & RSI Trading Strategy for {ticker}',
        xaxis_title='Dates',
        yaxis_title='Price in USD',
        template='plotly_white'
    )

    # Convert the plot to HTML string
    html_str = pio.to_html(fig, full_html=False)
    return html_str

# Test the function
html_output = bollingBandsRSI_test("META", 200)

# Create a simple pywebview application
window = webview.create_window('Bollinger Bands & RSI Trading Strategy', html=html_output)
webview.start()
