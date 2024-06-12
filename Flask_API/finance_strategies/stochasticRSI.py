import numpy as np
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
from plotly.subplots import make_subplots
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



# Create an exponential Moving Average Indicator function
def EMA(data, period=20, column='Close'):
    return data[column].ewm(span=period, adjust=False).mean()

def StochRSI(data, period=14, column='Close'):
    delta = data[column].diff(1)
    delta = delta.dropna()
    up = delta.copy()
    down = delta.copy()
    up[up<0]=0
    down[down>0]=0
    data['up']=up
    data['down']=down
    AVG_Gain = EMA(data, period, column='up')
    AVG_Loss = abs(EMA(data, period, column='down'))
    RS= AVG_Gain/AVG_Loss
    RSI = 100.0/(100.0/(1.0+RS))

    stockrsi = (RSI - RSI.rolling(period).min()) / (RSI.rolling(period).max() - RSI.rolling(period).min())
    return stockrsi


def get_StochRSI(ticker, days):

    df = get_stock_data(ticker, days)
    # Store the Stochastic RSI data in a new column
    df['StochRSI'] = StochRSI(df)

    # Create a figure and subplot using Plotly
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.1)

    # Plot the closing price
    fig.add_trace(go.Scatter(x=df.index, y=df['Close'], mode='lines', name='Close', line=dict(color='red')), row=1, col=1)

    # Plot the Stochastic RSI
    fig.add_trace(go.Scatter(x=df.index, y=df['StochRSI'], mode='lines', name='StochRSI', line=dict(color='blue', dash='dash')), row=2, col=1)

    # Add oversold and overbought lines
    fig.add_hline(y=0.20, line=dict(color='orange'), row=2, col=1)
    fig.add_hline(y=0.80, line=dict(color='orange'), row=2, col=1)

    # Update layout
    fig.update_layout(
        title=f'Stochastic RSI for {ticker}',
        xaxis_title='Date',
        yaxis_title='Price',
        template='plotly_white',
        height=800,
        width=1200,
        plot_bgcolor='lightgrey',
        paper_bgcolor='grey',
        font=dict(color='white')
    )
    ticks = round(days/2)
    # # Rotate x-axis labels
    fig.update_xaxes(tickangle=45,nticks=ticks, row=2, col=1)

        # Rotate x-axis labels and increase tick frequency
    # fig.update_xaxes(tickangle=45, tickmode='linear', nticks=5, row=1, col=1)  # Adjust 'nticks' to your desired number of ticks
    # fig.update_xaxes(tickangle=45, tickmode='linear', nticks=5, row=2, col=1)  # Ensure both subplots have the same x-axis settings

    # Show the plot
    html_str = pio.to_html(fig, full_html=False)
    return html_str
