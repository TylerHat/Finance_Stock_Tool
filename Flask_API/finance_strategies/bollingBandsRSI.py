import pandas as pd
import numpy as np
import yfinance as yf
import json

def testing():
    print("helloWorld")

def bollinger_bands(data, window_size=30):
    """
    Calculate Bollinger Bands for the given data.
    
    :param data: DataFrame containing stock data
    :param window_size: The window size for calculating the moving average and standard deviation
    :return: DataFrame with UpperBand and LowerBand columns added
    """
    rolling_mean = data['Close'].rolling(window=window_size).mean()
    rolling_std = data['Close'].rolling(window=window_size).std()
    data['UpperBand'] = rolling_mean + (2 * rolling_std)
    data['LowerBand'] = rolling_mean - (2 * rolling_std)
    return data

def rsi(data, window=14):
    """
    Calculate the Relative Strength Index (RSI) for the given data.
    
    :param data: DataFrame containing stock data
    :param window: The window size for calculating the RSI
    :return: DataFrame with RSI, Overbought, and Oversold columns added
    """
    delta = data['Close'].diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    avg_gain = gain.rolling(window=window).mean()
    avg_loss = loss.rolling(window=window).mean()
    rs = avg_gain / avg_loss
    data['RSI'] = 100 - (100 / (1 + rs))
    data['Overbought'] = 70
    data['Oversold'] = 30
    return data

def strategy(data):
    """
    Implement the trading strategy based on Bollinger Bands and RSI.
    
    :param data: DataFrame containing stock data with Bollinger Bands and RSI
    :return: Lists of buy and sell prices
    """
    position = 0
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

def get_stock_data(ticker, days):
    """
    Fetch historical stock data for the given ticker and number of days.
    
    :param ticker: The stock ticker symbol
    :param days: The number of days of historical data to fetch
    :return: DataFrame containing the stock data
    """
    end_date = pd.to_datetime('today')
    start_date = end_date - pd.Timedelta(days=days)
    stock_data = yf.download(ticker, start=start_date, end=end_date)
    return stock_data

def bollingBandsRSI_depricated(ticker, days):
    """
    Fetch stock data, calculate Bollinger Bands and RSI, and return the trading strategy data points as JSON.
    
    :param ticker: The stock ticker symbol
    :param days: The number of days of historical data to fetch
    :return: JSON string containing the x and y axis data points
    """
    data = get_stock_data(ticker, days)
    data = bollinger_bands(data)
    data = rsi(data)
    buy_price, sell_price = strategy(data)
    data['Buy'] = buy_price
    data['Sell'] = sell_price

    result = {
        'dates': data.index.strftime('%Y-%m-%d').tolist(),
        'close': data['Close'].tolist(),
        'upper_band': data['UpperBand'].tolist(),
        'lower_band': data['LowerBand'].tolist(),
        'buy_signals': data['Buy'].tolist(),
        'sell_signals': data['Sell'].tolist(),
    }

    return json.dumps(result)

def bollingBandsRSI(ticker, days):
    # Get the stock data for the given ticker and number of days
    data = get_stock_data(ticker, days)
    
    # Calculate Bollinger Bands
    data = bollinger_bands(data)
    
    # Calculate RSI
    data = rsi(data)
    
    # Apply the trading strategy to get buy and sell signals
    buy_price, sell_price = strategy(data)
    data['Buy'] = buy_price
    data['Sell'] = sell_price

    # Prepare the result in the desired format
    result = {}
    for date in data.index:
        result[date.strftime('%Y-%m-%d')] = {
            'close': data.loc[date, 'Close'],
            'upper_band': data.loc[date, 'UpperBand'],
            'lower_band': data.loc[date, 'LowerBand'],
            'buy_signal': data.loc[date, 'Buy'],
            'sell_signal': data.loc[date, 'Sell']
        }

    # Convert the result dictionary to a JSON string with indentation for readability
    result_json = json.dumps(result, indent=4)

    return result_json