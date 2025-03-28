from flask import Flask, render_template, jsonify
import os
from dotenv import load_dotenv
from utils import load_data, save_data, predict_next_period, get_food_recommendations

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Root Route
@app.route("/")
def home():
    data = load_data()
    next_period = predict_next_period(data)
    return render_template("index.html", data=data, next_period=next_period)

# Route to fetch food recommendations
@app.route("/recommendations/<phase>")
def food_recommendations(phase):
    recommendations = get_food_recommendations(phase)
    return jsonify(recommendations)

if __name__ == "__main__":
    app.run(debug=True)