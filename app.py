from flask import Flask, render_template, jsonify, request
import os
from dotenv import load_dotenv
from utils import load_data, save_data, predict_next_period, get_food_recommendations

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Root Route
@app.route("/")
def home():
    # Load cycle data and predict the next period
    data = load_data()
    next_period = predict_next_period(data)
    
    # Pass data to the frontend for rendering
    return render_template("index.html", data=data, next_period=next_period)

# Route to log a new menstrual cycle date
@app.route("/log-cycle", methods=["POST"])
def log_cycle():
    try:
        # Get the new cycle date from the request
        new_date = request.json.get("date")
        
        if not new_date:
            return jsonify({"error": "Date is required"}), 400
        
        # Load existing data, append the new date, and save
        data = load_data()
        data.append(new_date)
        save_data(data)
        
        # Predict the next period based on updated data
        next_period = predict_next_period(data)
        return jsonify({"message": "Cycle logged successfully", "next_period": next_period}), 200
    
    except Exception as e:
        return jsonify({"error": f"Failed to log cycle: {str(e)}"}), 500

# Route to fetch food recommendations
@app.route("/recommendations/<phase>")
def food_recommendations(phase):
    # Fetch food recommendations based on the phase
    recommendations = get_food_recommendations(phase)
    
    # Return the recommendations as JSON
    return jsonify(recommendations)

if __name__ == "__main__":
    app.run(debug=True)