from datetime import datetime
import pandas as pd
import random
from statsmodels.tsa.arima.model import ARIMA
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import matplotlib.pyplot as plt
from tabulate import tabulate

# Download NLTK data
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('averaged_perceptron_tagger')

# Generate synthetic data for demonstration
def generate_synthetic_data(commodity, weeks=52):
    prices = [random.uniform(50, 100) for _ in range(weeks)]
    return pd.DataFrame({
        'Week': pd.date_range(start='2024-01-01', periods=weeks, freq='W'),
        commodity: prices
    })

# Generate synthetic data for different commodities
diesel_data = generate_synthetic_data('Diesel')
petroleum_data = generate_synthetic_data('Petroleum')
lng_data = generate_synthetic_data('Lng')

# Merge all commodities into one DataFrame
commodities_data = diesel_data.merge(petroleum_data, on='Week').merge(lng_data, on='Week')

# Convert 'Week' to datetime and set as index
commodities_data['Week'] = pd.to_datetime(commodities_data['Week'])
commodities_data.set_index('Week', inplace=True)

# Debugging: Print the columns of the commodities_data DataFrame
print("Commodities Data Columns:", list(commodities_data.columns))

# Function to predict prices using ARIMA
def predict_prices(data, commodity, steps=10):
    series = data[commodity]

    # Fit ARIMA model
    model = ARIMA(series, order=(5, 1, 0))
    model_fit = model.fit()

    # Make forecast
    forecast = model_fit.forecast(steps=steps)
    forecast_dates = pd.date_range(start=series.index[-1], periods=steps + 1, freq='W')[1:]
    return dict(zip(forecast_dates, forecast))

# Function to plot predicted prices
def plot_forecast(forecast, commodity):
    dates = list(forecast.keys())
    prices = list(forecast.values())

    plt.figure(figsize=(10, 5))
    plt.plot(dates, prices, marker='o', linestyle='-', color='b')
    plt.title(f'Predicted Prices for {commodity}')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.grid(True)
    plt.show()

# Function to provide advice on hedging or speculating
def hedge_or_speculate(forecast):
    prices = list(forecast.values())
    if prices[-1] > prices[0]:
        return "Based on the predicted prices, it is advisable to speculate."
    else:
        return "Based on the predicted prices, it is advisable to hedge."

# Function to display possible queries in a table
def display_help():
    queries = [
        ["Query", "Description"],
        ["What is the current price of <commodity>?", "Get the current price of a commodity."],
        ["What are the predictions for <commodity>?", "Get the price predictions for a commodity."],
        ["Should I hedge or speculate on <commodity>?", "Get advice on whether to hedge or speculate based on price predictions."],
        ["Show historical prices for <commodity>", "Get the historical prices for a commodity."],
        ["Help", "Display this help message."],
        ["Exit or Quit", "Exit the chatbot."]
    ]
    return tabulate(queries, headers="firstrow", tablefmt="grid")

# Function to handle user messages
def handle_message(user_message):
    user_message = user_message.lower()
    tokens = word_tokenize(user_message)
    tokens = [word for word in tokens if word.isalnum()]
    filtered_tokens = [word for word in tokens if word not in stopwords.words('english')]
    
    response = ""

    # Identify the commodity
    commodity = next((word.capitalize() for word in filtered_tokens if word.capitalize() in commodities_data.columns or word.upper() in commodities_data.columns), None)
    # Debugging: Print the identified commodity
    print("Identified Commodity:", commodity)

    if any(greet in filtered_tokens for greet in ["hello", "hi", "hey"]):
        response = "Hello! How can I assist you with energy prices today?"
    elif "price" in filtered_tokens or "prices" in filtered_tokens:
        if commodity:
            current_price = commodities_data[commodity].iloc[-1]
            response = f"The current price of {commodity} is ${current_price:.2f}."
        else:
            response = "Sorry, I don't have data for that commodity."
    elif "predict" in filtered_tokens or "predictions" in filtered_tokens:
        if commodity:
            forecast = predict_prices(commodities_data, commodity, steps=10)
            response = f"Predicted prices for {commodity}:\n"
            response += "\n".join([f"{date.date()}: ${price:.2f}" for date, price in forecast.items()])
            plot_forecast(forecast, commodity)
            advice = hedge_or_speculate(forecast)
            response += f"\n{advice}"
        else:
            response = "Sorry, I don't have data for that commodity."
    elif "hedge" in filtered_tokens or "speculate" in filtered_tokens:
        if commodity:
            forecast = predict_prices(commodities_data, commodity, steps=10)
            advice = hedge_or_speculate(forecast)
            response = f"{advice}"
        else:
            response = "Sorry, I don't have data for that commodity."
    elif "history" in filtered_tokens or "historical" in filtered_tokens:
        if commodity:
            historical_data = commodities_data[commodity].tail(10)
            response = f"Historical prices for {commodity}:\n"
            response += "\n".join([f"{date.date()}: ${price:.2f}" for date, price in historical_data.items()])
        else:
            response = "Sorry, I don't have data for that commodity."
    elif "help" in filtered_tokens:
        response = display_help().replace('\n', '\n')
    else:
        response = "I can provide energy price predictions! Try asking about current prices, predictions, or historical data."

    return response

# Main function to run the chatbot
def main():
    current_date = input("Please enter the current date (YYYY-MM-DD): ")
    try:
        current_date = datetime.strptime(current_date, "%Y-%m-%d")
    except ValueError:
        print("Invalid date format. Using default start date '2024-01-01'.")
        current_date = datetime.strptime("2024-01-01", "%Y-%m-%d")
    print("Welcome to the Energy Chatbot!")
    print("You can ask about current prices, predictions, or historical data for Diesel, Petroleum, and LNG.")
    print("Type 'help' for more information.")
    try:
        while True:
            user_message = input("You: ")
            if user_message.lower() in ["exit", "quit"]:
                print("Goodbye!")
                break
            response = handle_message(user_message)
            print(f"Bot: {response}")
    except KeyboardInterrupt:
        print("\nGoodbye!")

if __name__ == "__main__":
    main()