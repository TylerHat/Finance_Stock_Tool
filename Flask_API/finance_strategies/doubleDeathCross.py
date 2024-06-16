import pandas as pd
import yfinance as yf

def get_stock_data(ticker: str, days: int) -> pd.DataFrame:
    # Calculate the start date based on the number of days
    end_date = pd.to_datetime('today')
    start_date = end_date - pd.Timedelta(days=days)
    
    # Fetch the data using yfinance
    stock_data = yf.download(ticker, start=start_date, end=end_date)
    
    return stock_data

def get_doubleDeathCross(ticker, days):
    stock_data = get_stock_data(ticker, days)

    # Calculate SMAs
    stock_data['SMA_50'] = stock_data['Close'].rolling(window=50).mean()
    stock_data['SMA_200'] = stock_data['Close'].rolling(window=200).mean()

    # Generate buy/sell signals
    stock_data['Signal'] = 0

    # If the current 50-day SMA crossed below the current 200-day SMA and the previous 50-day SMA crossed above the previous SMA, then sell (indicate = -1)
    stock_data.loc[(stock_data['SMA_50'] <= stock_data['SMA_200']) & (stock_data['SMA_50'].shift(1) > stock_data['SMA_200'].shift(1)), 'Signal'] = -1

    # If the current 50-day SMA crossed above the current 200-day SMA and the previous 50-day SMA crossed below the previous SMA, then buy (indicate = 1)
    stock_data.loc[(stock_data['SMA_50'] >= stock_data['SMA_200']) & (stock_data['SMA_50'].shift(1) < stock_data['SMA_200'].shift(1)), 'Signal'] = 1

    stock_data.dropna(inplace=True)

    # Prepare the data for JSON output
    output = {
        'dates': stock_data.index.strftime('%Y-%m-%d').tolist(),
        'close': stock_data['Close'].tolist(),
        'SMA_50': stock_data['SMA_50'].tolist(),
        'SMA_200': stock_data['SMA_200'].tolist(),
        'buy_signals': stock_data[stock_data['Signal'] == 1].index.strftime('%Y-%m-%d').tolist(),
        'sell_signals': stock_data[stock_data['Signal'] == -1].index.strftime('%Y-%m-%d').tolist(),
    }

    return output
