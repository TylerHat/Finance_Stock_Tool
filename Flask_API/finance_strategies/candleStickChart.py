import plotly.graph_objects as go
import yfinance as yf
import pandas as pd
import plotly.io as pio
import mpld3

def get_stock_data(ticker: str, days: int) -> pd.DataFrame:
    """
    Fetches the Open, High, Low, Close, Adjusted Close, and Volume data for a given stock ticker and number of days.

    :param ticker: The stock ticker symbol.
    :param days: The number of days of historical data to fetch.
    :return: A pandas DataFrame containing the stock data.
    """
    # Calculate the start date based on the number of days
    end_date = pd.to_datetime('today')
    start_date = end_date - pd.Timedelta(days=days)
    
    # Fetch the data using yfinance
    stock_data = yf.download(ticker, start=start_date, end=end_date)
    
    return stock_data
def get_candlestickchart(ticker, days):

    df = get_stock_data(ticker, days)

    #create interactive candlestick chart
    fig = go.Figure(
        data = [
            go.Candlestick(
                title=f'Candlestick Chart for {ticker}',
                x = df.index,
                low = df['Low'], 
                high = df['High'], 
                close = df['Close'],
                open = df['Open'], 
                increasing_line_color = 'green',
                decreasing_line_color = 'red'
            )
        ]
    )
    html_str = pio.to_html(fig, full_html=False)
    return html_str