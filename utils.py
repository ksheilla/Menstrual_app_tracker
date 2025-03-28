import os
import json
from datetime import datetime, timedelta
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Define the data file path
DATA_FILE = os.path.join(os.path.dirname(__file__), "data", "cycle_data.json")

def load_data():
    """Load cycle data from JSON file"""
    if not os.path.exists(DATA_FILE):
        os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
        return []
    
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return []

def save_data(data):
    """Save cycle data to JSON file"""
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

def predict_next_period(data):
    """Predict the next period date"""
    if len(data) < 2:
        return None

    cycle_lengths = [
        (datetime.strptime(data[i], "%Y-%m-%d") - datetime.strptime(data[i - 1], "%Y-%m-%d")).days
        for i in range(1, len(data))
    ]
    avg_cycle_length = sum(cycle_lengths) / len(cycle_lengths)
    last_period = datetime.strptime(data[-1], "%Y-%m-%d")
    next_period = last_period + timedelta(days=avg_cycle_length)
    return next_period.strftime("%Y-%m-%d")

def get_food_recommendations(phase):
    """Fetch food recommendations from Spoonacular API"""
    # Get API key
    api_key = os.getenv("SPOONACULAR_API_KEY")
    
    if not api_key:
        return {"error": "Spoonacular API key is missing"}

    query = {
        "menstruation": "iron-rich foods",
        "follicular": "hormone-balancing foods",
        "ovulation": "high-protein foods",
        "luteal": "mood-supporting foods"
    }.get(phase, "balanced diet")

    url = "https://spoonacular.com/food-api"
    params = {
        "apiKey": api_key,
        "query": query,
        "number": 5,
        "instructionsRequired": True,
        "addRecipeInformation": True,
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        # Extract relevant recipe information
        recipes = [
            {
                "title": recipe.get("title", "Unknown Recipe"),
                "image": recipe.get("image", ""),
                "sourceUrl": recipe.get("sourceUrl", ""),
                "readyInMinutes": recipe.get("readyInMinutes", 0)
            } for recipe in data.get("results", [])
        ]
        
        return recipes
    
    except requests.RequestException as e:
        print(f"API Request Error: {e}")
        return {"error": f"Failed to fetch food recommendations: {str(e)}"}