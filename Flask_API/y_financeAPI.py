from flask import Flask, jsonify, request
from finance_strategies.bollingBandsRSI import bollingBandsRSI
from finance_strategies.bollingBandsRSI_html import bollingBandsRSI_test
from finance_strategies.candleStickChart import get_candlestickchart
from finance_strategies.sharpeRatioCalc import get_sharpeRatioCalc
from finance_strategies.stochasticRSI import get_StochRSI
from finance_strategies.doubleDeathCross import get_doubleDeathCross
from markupsafe import escape
import json
import yfinance as yf
from datetime import datetime, timedelta


#docker build -t thatfield123/financial_info_1:latest .
#docker container run -d -p 3000:3000 thatfield123/financial_info_1:latest
 
app = Flask(__name__)
 
def format_timestamps(data):
    formatted_data = {str(date): price for date, price in data.items()}
    return formatted_data
 
@app.route('/test')

def hello_world():
    return "<h1>API twfsdfhgsd Display</h1>"
##--------------------------------Actual Graph Endpoint for React-------------------
@app.route('/get_bollingBandsRSI/<ticker>/<int:days>', methods=['GET'])
def plot_bollinger_endpoint(ticker, days):
    plot_bollinger = bollingBandsRSI(ticker, days)
    return jsonify(json.loads(plot_bollinger))

@app.route('/get_sharpeRatio/<ticker>/<int:days>', methods=['GET'])
def get_sharpeRatio(ticker, days):
    plot_sharpeRatio = get_sharpeRatioCalc(ticker, days)
    return plot_sharpeRatio

@app.route('/get_doubleDeathCross/<ticker>/<int:days>', methods=['GET'])
def get_doubleDeathCrossgraph(ticker, days):
    doubleDeathCrossgraph = get_doubleDeathCross(ticker, days)
    return jsonify(doubleDeathCrossgraph)






 
# Endpoint to get company info
@app.route('/company_info/<ticker>', methods=['GET'])

def company_info(ticker):
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        return jsonify(info)

    except Exception as e:
        return jsonify({'error': str(e)}), 500
 
# Endpoint to get current stock price

@app.route('/current_price/<ticker>', methods=['GET'])

def current_price(ticker):
    try:
        stock = yf.Ticker(ticker)
        current_price = stock.history(period='1d')['Close'].iloc[-1]
        return jsonify({'ticker': ticker, 'current_price': current_price})
   
    except Exception as e:
        return jsonify({'error': str(e)}), 500
 
def format_timestamps(data):
    # This function converts the timestamps to a more readable format if needed.
    # Modify this function as needed to format your timestamps.
    return {str(k): v for k, v in data.items()}
 
@app.route('/historical_prices/<ticker>/<days>', methods=['GET'])

def historical_prices(ticker, days):
    try:
        stock = yf.Ticker(ticker)
        end_date = datetime.now()
        start_date = end_date - timedelta(int(days))
        hist = stock.history(start=start_date, end=end_date)
       
        # Extract the required data
        closing_prices = hist['Close'].to_dict()
        opening_prices = hist['Open'].to_dict()
        high_prices = hist['High'].to_dict()
        low_prices = hist['Low'].to_dict()

        # Format the data
        formatted_closing_prices = format_timestamps(closing_prices)
        formatted_opening_prices = format_timestamps(opening_prices)
        formatted_high_prices = format_timestamps(high_prices)
        formatted_low_prices = format_timestamps(low_prices)

        # Combine the data into a single table
        combined_data = {}

        for date in formatted_closing_prices.keys():
            combined_data[date] = {
                'opening_price': formatted_opening_prices.get(date),
                'high_price': formatted_high_prices.get(date),
                'low_price': formatted_low_prices.get(date),
                'closing_price': formatted_closing_prices.get(date)
            }

        return jsonify(combined_data)

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/grag/plot_bollingBandsRSI/<ticker>/<int:days>', methods=['GET'])
def graph_plot_bollinger_endpoint(ticker, days):
    plot_bollinger = bollingBandsRSI_test(ticker, days)
    return plot_bollinger

@app.route('/g/plot_candlestickchart/<ticker>/<int:days>', methods=['GET'])
def plot_candlestick_endpoint(ticker, days):
    plot_candle = get_candlestickchart(ticker, days)
    return plot_candle



@app.route('/g/get_stochRSI/<ticker>/<int:days>', methods=['GET'])
def get_stochRSIRatio(ticker, days):
    plot_stochRSIRatio = get_StochRSI(ticker, days)
    return plot_stochRSIRatio

# @app.route('/g/get_doubleDeathCross/<ticker>/<int:days>', methods=['GET'])
# def get_doubleDeathCrossgraph(ticker, days):
#     doubleDeathCrossgraph = get_doubleDeathCross(ticker, days)
#     return doubleDeathCrossgraph
        
if __name__ == "__main__":
        app.run(host="0.0.0.0", port=int("5000"), debug=True)