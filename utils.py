import os
import json
from datetime import datetime, timedelta
import requests

# Function to load cycle data
def load_data():
    DATA_FILE = "data/cycle_data.json"
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as f:
        return json.load(f)

# Function to save cycle data
def save_data(data):
    DATA_FILE = "data/cycle_data.json"
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

# Function to predict next period
def predict_next_period(data):
    if len(data) < 2:
        return None

    cycle_lengths = [
        (datetime.strptime(data[i], "%Y-%m-%d") - datetime.strptime(data[i - 1], "%Y-%m-%d")).days
        for i in range(1, len(data))
    ]
    avg_cycle_length = sum(cycle_lengths) / len(cycle_lengths)
    last_period = datetime.strptime(data[-1], "%Y-%m-%d")
    return (last_period + timedelta(days=avg_cycle_length)).strftime("%Y-%m-%d")

# Function to get food recommendations based on cycle phase
def get_food_recommendations(phase):
    query = {
        "menstruation": "iron-rich foods",
        "ovulation": "high-protein foods"
    }.get(phase, "balanced diet")

    url = "https://api.spoonacular.com/recipes/complexSearch"
    params = {
        "apiKey": SPOONACULAR_API_KEY,
        "query": query,
        "number": 5,  # Fetch 5 recommendations
        "instructionsRequired": True,
        "addRecipeInformation": True,
    }

    response = requests.get(url, params=params)
    print(f"Response status code: {response.status_code}")  # Debugging
    print(f"Response content: {response.text}")  # Debugging

    if response.status_code == 200:
        return response.json().get("results", [])
    return {"error": "Failed to fetch food recommendations."}
