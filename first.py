import requests
import json

# API URL for the energy market data
ENERGY_API_URL = "https://api.energy-market.com/data"  # Replace with actual API endpoint

# Placeholder API key or authentication token
API_KEY = "your_api_key_here"

# Function to get energy market data from API
def get_energy_market_data():
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    response = requests.get(ENERGY_API_URL, headers=headers)

    if response.status_code == 200:
        data = response.json()  # Assuming the API returns JSON data
        return data
    else:
        return None

# Function to process and analyze energy market data
def analyze_energy_data(data):
    # Example: Extracting specific data points (adjust based on actual API response)
    price = data.get("price", "N/A")
    demand = data.get("demand", "N/A")
    supply = data.get("supply", "N/A")
    
    # Example analysis
    if price > 100:
        analysis = "Energy prices are high. Consider optimizing usage or exploring alternatives."
    elif price < 50:
        analysis = "Energy prices are low. It might be a good time to increase consumption."
    else:
        analysis = "Energy prices are moderate."

    return f"Price: {price} USD/MWh, Demand: {demand} MW, Supply: {supply} MW. {analysis}"

# Function to handle user queries
def handle_user_input(user_input):
    if "energy prices" in user_input.lower():
        data = get_energy_market_data()
        if data:
            analysis = analyze_energy_data(data)
            return analysis
        else:
            return "Sorry, I couldn't fetch the data at the moment. Please try again later."
    else:
        return "I'm here to help you with energy market analysis. Ask me about energy prices, demand, or supply."

# Main chatbot loop
def chatbot():
    print("Welcome to the Energy Market Analysis Chatbot!")
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            print("Goodbye!")
            break
        response = handle_user_input(user_input)
        print(f"Chatbot: {response}")

# Run the chatbot
if __name__ == "__main__":
    chatbot()


