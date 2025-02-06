# stock_predictor.py
import yfinance as yf
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from datetime import datetime, timedelta

# Fetch real-time stock data for a given stock symbol
def fetch_real_time_stock_data(stock_symbol):
    stock_data = yf.download(stock_symbol, period="1mo", interval="1d")
    stock_price = stock_data['Close'][-1]
    return stock_price, stock_data

# Simple stock recommendation model based on user inputs
def get_stock_recommendation(income, target_return):
    # Define some sample stock symbols to choose from
    stock_symbols = ["AAPL", "GOOGL", "AMZN", "MSFT", "TSLA"]
    
    best_stock = None
    best_predicted_return = 0
    
    # Loop through each stock symbol to predict and find the best return
    for stock_symbol in stock_symbols:
        stock_price, stock_data = fetch_real_time_stock_data(stock_symbol)
        
        # Simple prediction: Use the last month's data to predict the next 3 months (for example)
        stock_data['Date'] = pd.to_datetime(stock_data.index)
        stock_data['Days'] = (stock_data['Date'] - stock_data['Date'].min()).dt.days
        
        # Using Linear Regression to predict future price
        model = LinearRegression()
        X = stock_data[['Days']]
        y = stock_data['Close']
        model.fit(X, y)
        
        # Predict stock price in 3 months
        future_days = (datetime.now() + timedelta(days=90)).day - stock_data['Date'].min().days
        predicted_price = model.predict([[future_days]])[0]
        
        predicted_return = (predicted_price - stock_price) / stock_price * 100
        
        # Choose the stock with the best predicted return
        if predicted_return > best_predicted_return:
            best_predicted_return = predicted_return
            best_stock = {
                "stock_name": stock_symbol,
                "stock_price": stock_price,
                "predicted_return": predicted_return
            }

    return best_stock
