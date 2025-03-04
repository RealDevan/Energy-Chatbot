import numpy as np
import pandas as pd
import random
from statsmodels.tsa.arima.model import ARIMA
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

# Download NLTK data
nltk.download('punkt')
nltk.download('stopwords')

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
lng_data = generate_synthetic_data('LNG')
nat_gas_data = generate_synthetic_data('Natural Gas')

# Merge all commodities into one DataFrame
commodities_data = diesel_data.merge(petroleum_data, on='Week').merge(lng_data, on='Week').merge(nat_gas_data, on='Week')

# Convert 'Week' to datetime and set as index
commodities_data['Week'] = pd.to_datetime(commodities_data['Week'])
commodities_data.set_index('Week', inplace=True)

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

# Function to handle user messages
def handle_message(user_message):
    user_message = user_message.lower()
    tokens = word_tokenize(user_message)
    tokens = [word for word in tokens if word.isalnum()]
    filtered_tokens = [word for word in tokens if word not in stopwords.words('english')]
    
    response = ""

    if "price" in filtered_tokens:
        commodity = filtered_tokens[-1]
        if commodity.capitalize() in commodities_data.columns:
            current_price = commodities_data[commodity.capitalize()].iloc[-1]
            response = f"The current price of {commodity.capitalize()} is ${current_price:.2f}."
        else:
            response = f"Sorry, I don't have data for {commodity.capitalize()}."
    elif "predict" in filtered_tokens:
        commodity = filtered_tokens[-1]
        if commodity.capitalize() in commodities_data.columns:
            forecast = predict_prices(commodities_data, commodity.capitalize(), steps=10)
            response = f"Predicted prices for {commodity.capitalize()}:\n"
            response += "\n".join([f"{date.date()}: ${price:.2f}" for date, price in forecast.items()])
        else:
            response = f"Sorry, I don't have data for {commodity.capitalize()}."
    elif "history" in filtered_tokens:
        commodity = filtered_tokens[-1]
        if commodity.capitalize() in commodities_data.columns:
            historical_data = commodities_data[commodity.capitalize()].tail(10)
            response = f"Historical prices for {commodity.capitalize()}:\n"
            response += "\n".join([f"{date.date()}: ${price:.2f}" for date, price in historical_data.items()])
        else:
            response = f"Sorry, I don't have data for {commodity.capitalize()}."
    elif "help" in filtered_tokens:
        response = ("I can provide energy price predictions and historical data!\n"
                    "Try asking about current prices, predictions, or historical data for Diesel, Petroleum, LNG, and Natural Gas.\n"
                    "You can also type 'exit' or 'quit' to end the conversation.")
    else:
        response = "I can provide energy price predictions! Try asking about current prices, predictions, or historical data."

    return response

# Main function to run the chatbot
def main():
    print("Welcome to the Energy Chatbot!")
    print("You can ask about current prices, predictions, or historical data for Diesel, Petroleum, LNG, and Natural Gas.")
    print("Type 'help' for more information.")
    while True:
        user_message = input("You: ")
        if user_message.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break
        response = handle_message(user_message)
        print(f"Bot: {response}")

if __name__ == "__main__":
    main()