#This program calculate the sharpe ratio. Measure of return which calcs the risk and 
# reward with past performaance and posible future performance

import pandas as pd
import numpy as np
import yfinance as yf

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

# Example usage
def get_sharpeRatioCalc(ticker, days):

    data = get_stock_data(ticker, days)

    #Calc the daily returns
    data['returns'] = data['Adj Close'].pct_change(1)

    #Define the risk free rate
    #0.02% returns on 252 trading days in a year
    risk_free_rate = 0.02/252
    
    #calc excess returns: how much more money you are supposed to make when investing in a stock/fund
    data['excess_return'] =data['returns'] - risk_free_rate

    #calc the Sharp Ratio:measure of return which calc the risk in achiving that return
    sharpe_ratio = np.sqrt(252) * data['excess_return'].mean() / data['excess_return'].std()

    #sharpe ratio below 1 is BAD, =1 is passing, >1 is good, >2 is great, 3> is exelent
    return str(sharpe_ratio)

