from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import pandas as pd
import numpy as np
import yfinance as yf

def bollinger_bands(data, window_size=30):
    rolling_mean = data['Close'].rolling(window=window_size).mean()
    rolling_std = data['Close'].rolling(window=window_size).std()
    data['UpperBand'] = rolling_mean + (2 * rolling_std)
    data['LowerBand'] = rolling_mean - (2 * rolling_std)
    return data

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

def strategy(data):
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

def get_stock_data(ticker: str, days: int) -> pd.DataFrame:
    end_date = pd.to_datetime('today')
    start_date = end_date - pd.Timedelta(days=days)
    stock_data = yf.download(ticker, start=start_date, end=end_date)
    stock_data.reset_index(inplace=True)
    return stock_data

@csrf_exempt
def bollinger_rsi_view(request):
    ticker = request.GET.get('ticker', 'META')
    days = int(request.GET.get('days', 50))

    data = get_stock_data(ticker, days)
    data = bollinger_bands(data)
    data = rsi(data)
    buy_price, sell_price = strategy(data)
    data['Buy'] = buy_price
    data['Sell'] = sell_price

    json_data = {
        'Date': data['Date'].dt.strftime('%Y-%m-%d').tolist(),
        'Close': data['Close'].tolist(),
        'UpperBand': data['UpperBand'].tolist(),
        'LowerBand': data['LowerBand'].tolist(),
        'RSI': data['RSI'].tolist(),
        'Buy': data['Buy'].tolist(),
        'Sell': data['Sell'].tolist(),
    }

    return JsonResponse(json_data)
