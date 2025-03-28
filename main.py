import os
import json
from datetime import datetime, timedelta

DATA_FILE = "data/cycle_data.json"

def load_data():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

def add_cycle_entry(start_date):
    try:
        start_date = datetime.strptime(start_date, "%Y-%m-%d")
    except ValueError:
        print("Invalid date format. Please use YYYY-MM-DD.")
        return

    data = load_data()
    data.append(start_date.strftime("%Y-%m-%d"))
    save_data(data)
    print("Cycle entry added successfully.")

def predict_next_period():
    data = load_data()
    if len(data) < 2:
        print("Not enough data to predict the next period. Please log at least two cycle entries.")
        return

    # Calculate average cycle length
    cycle_lengths = [
        (datetime.strptime(data[i], "%Y-%m-%d") - datetime.strptime(data[i - 1], "%Y-%m-%d")).days
        for i in range(1, len(data))
    ]
    avg_cycle_length = sum(cycle_lengths) / len(cycle_lengths)

    # Predict next period
    last_period = datetime.strptime(data[-1], "%Y-%m-%d")
    next_period = last_period + timedelta(days=avg_cycle_length)
    print(f"Next period is predicted to start on: {next_period.strftime('%Y-%m-%d')}")

def view_cycle_history():
    data = load_data()
    if not data:
        print("No cycle data available.")
        return

    print("Cycle History:")
    for i, date in enumerate(data):
        print(f"{i + 1}. {date}")

def delete_cycle_entry():
    data = load_data()
    if not data:
        print("No cycle data available to delete.")
        return

    print("Cycle History:")
    for i, date in enumerate(data):
        print(f"{i + 1}. {date}")

    try:
        choice = int(input("Enter the number of the entry you want to delete: "))
        if 1 <= choice <= len(data):
            deleted_entry = data.pop(choice - 1)  # Remove the selected entry
            save_data(data)
            print(f"Deleted entry: {deleted_entry}")
        else:
            print("Invalid choice. Please select a valid entry number.")
    except ValueError:
        print("Invalid input. Please enter a number.")

def main():
    while True:
        print("\n--- Menstrual Cycle Tracker ---")
        print("1. Add Cycle Entry")
        print("2. Predict Next Period")
        print("3. View Cycle History")
        print("4. Delete Cycle Entry")
        print("5. Exit")
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            start_date = input("Enter the start date of your last period (YYYY-MM-DD): ").strip()
            add_cycle_entry(start_date)
        elif choice == "2":
            predict_next_period()
        elif choice == "3":
            view_cycle_history()
        elif choice == "4":
            delete_cycle_entry()
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()