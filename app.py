from flask import Flask, render_template, request, jsonify
import os
from dotenv import load_dotenv
from utils import load_data, save_data, predict_next_period, get_food_recommendations  # Importing functions from utils.py

# Load environment variables
load_dotenv()
SPOONACULAR_API_KEY = os.getenv("SPOONACULAR_API_KEY")

if not SPOONACULAR_API_KEY:
    raise ValueError("❌ API Key not found! Make sure .env file exists and contains SPOONACULAR_API_KEY.")

print(f"✅ Loaded API Key: {SPOONACULAR_API_KEY}")  # Debugging

app = Flask(__name__)

# Root Route ("/")
@app.route("/")
def home():
    # This should render the template, not return a string after it
    data = load_data()
    next_period = predict_next_period(data)
    return render_template("index.html", data=data, next_period=next_period)

# Route to fetch food recommendations
@app.route("/recommendations/<phase>")
def food_recommendations(phase):
    recommendations = get_food_recommendations(phase)
    if "error" in recommendations:
        return jsonify({"error": recommendations["error"]}), 400
    return jsonify(recommendations)

# Route to handle cycle tracking (POST method)
@app.route("/cycle", methods=["POST"])
def track_cycle():
    data = request.get_json()
    start_date = data.get("start_date")

    try:
        start_date = datetime.strptime(start_date, "%Y-%m-%d").strftime("%Y-%m-%d")
    except ValueError:
        return jsonify({"error": "Invalid date format. Please use YYYY-MM-DD."}), 400

    # Save new cycle entry
    saved_data = load_data()
    saved_data.append(start_date)
    save_data(saved_data)

    return jsonify({"message": "Cycle entry added successfully."}), 200

# Run Flask app
if __name__ == "__main__":
    app.run(debug=True)

