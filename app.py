import yfinance as yf
from flask import Flask, render_template, request
import datetime

app = Flask(__name__)

@app.route('/')
def home():
    # Provide default values for templates variables:
    return render_template('index.html', recommendations=None, stock_trends={}, months=0, advice=[])

@app.route('/recommend', methods=['POST'])
def recommend():
    # Get user input
    income = int(request.form['income'])
    return_target = int(request.form['return_target'])
    months = int(request.form['months'])
    
    # Define stock symbols (user can select from a list)
    stocks = ['AAPL', 'GOOGL', 'AMZN', 'MSFT']

    # Recommendations and Stock Data
    recommendations = []
    stock_trends = {}

    # Date range for historical data (last 3 months)
    end_date = datetime.datetime.today()
    start_date = end_date - datetime.timedelta(days=months*30)

    for stock in stocks:
        stock_data = yf.Ticker(stock)
        
        # Fetch historical stock data for the past 'months' period
        history = stock_data.history(start=start_date, end=end_date)
        stock_prices = history['Close'].tolist()

        # Calculate current stock price and estimated return
        current_price = stock_prices[-1]  # Most recent closing price
        estimated_return = current_price * (return_target / 100)  # Example return calculation

        # Store data for chart rendering
        stock_trends[stock] = stock_prices

        recommendations.append({
            'stock': stock,
            'current_price': current_price,
            'estimated_return': estimated_return
        })
    
    # Advice generation based on user's income and return target
    advice = generate_advice(income, return_target)

    return render_template('index.html', 
                           recommendations=recommendations, 
                           stock_trends=stock_trends, 
                           user_income=income, 
                           return_target=return_target, 
                           advice=advice)

def generate_advice(income, return_target):
    """
    Generate personalized investment advice based on income and return target.
    """
    advice = []
    
    if income < 50000:
        advice.append("With a lower income, you may want to start with safer, lower-risk investments.")
        advice.append("Consider investing in index funds or blue-chip stocks with steady returns.")
        advice.append("Focus on building wealth over time rather than high-risk, high-return stocks.")
    elif income >= 50000 and return_target < 10:
        advice.append("With a moderate income and lower return expectations, consider a diversified portfolio.")
        advice.append("You can balance between growth stocks and safer investments like bonds.")
        advice.append("Index funds and large-cap stocks are good options to minimize risk while earning steady returns.")
    else:
        advice.append("With a higher income and a higher return target, you may consider growth stocks.")
        advice.append("Investing in tech and emerging sectors can yield high returns but comes with increased risk.")
        advice.append("Diversify your portfolio to manage risk, but aim for higher growth in key sectors.")

    return advice

if __name__ == "__main__":
    app.run(debug=True)
