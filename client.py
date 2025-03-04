import requests

url = "http://127.0.0.1:5000/chat"

while True:
    user_input = input("You: ")
    if user_input.lower() in ["exit", "quit"]:
        print("Chatbot: Goodbye!")
        break
    
    response = requests.post(url, json={"message": user_input})
    print("Chatbot:", response.json()["response"])