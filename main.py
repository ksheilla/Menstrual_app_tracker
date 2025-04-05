import os
import json
from datetime import datetime, timedelta

DATA_FILE = "data/cycle_data.json"

def load_data():
    """Load cycle data with error handling and sorting"""
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
            # Sort dates chronologically
            return sorted(data, key=lambda x: datetime.strptime(x, "%Y-%m-%d"))
    except (json.JSONDecodeError, FileNotFoundError):
        print("Error loading data. Resetting to empty list.")
        return []

def save_data(data):
    """Save data with error handling and sorting"""
    try:
        # Sort before saving
        sorted_data = sorted(data, key=lambda x: datetime.strptime(x, "%Y-%m-%d"))
        os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
        with open(DATA_FILE, "w") as f:
            json.dump(sorted_data, f, indent=4)
    except Exception as e:
        print(f"Failed to save data: {e}")

def add_cycle_entry(start_date):
    """Add entry with validation and duplicate check"""
    try:
        new_date = datetime.strptime(start_date, "%Y-%m-%d").date()
    except ValueError:
        print("⚠️ Invalid date format. Please use YYYY-MM-DD.")
        return False

    data = load_data()
    
    # Check for duplicates
    if new_date.strftime("%Y-%m-%d") in data:
        print("⚠️ This date is already logged.")
        return False

    data.append(new_date.strftime("%Y-%m-%d"))
    save_data(data)
    print(f"✅ Entry added: {new_date.strftime('%Y-%m-%d')}")
    return True

def predict_next_period():
    """Improved prediction with sorted data and validation"""
    data = load_data()
    if len(data) < 2:
        print("⚠️ Not enough data to predict. Log at least 2 periods.")
        return

    try:
        # Ensure dates are sorted
        sorted_dates = sorted(data, key=lambda x: datetime.strptime(x, "%Y-%m-%d"))
        cycle_lengths = []
        for i in range(1, len(sorted_dates)):
            prev = datetime.strptime(sorted_dates[i-1], "%Y-%m-%d")
            curr = datetime.strptime(sorted_dates[i], "%Y-%m-%d")
            cycle_lengths.append((curr - prev).days)

        avg_length = round(sum(cycle_lengths) / len(cycle_lengths))
        last_period = datetime.strptime(sorted_dates[-1], "%Y-%m-%d")
        next_period = last_period + timedelta(days=avg_length)
        print(f"🔮 Next period predicted: {next_period.strftime('%Y-%m-%d')}")
        print(f"   (Average cycle length: {avg_length} days)")
        
    except Exception as e:
        print(f"⚠️ Prediction error: {e}")

def view_cycle_history():
    """Display history with index numbers"""
    data = load_data()
    if not data:
        print("📝 No cycle data available.")
        return

    print("🌸 Cycle History:")
    for idx, date in enumerate(data, 1):
        print(f"{idx}. {date}")

def delete_cycle_entry():
    """Delete entry with validation and confirmation"""
    data = load_data()
    if not data:
        print("⚠️ No entries to delete.")
        return

    view_cycle_history()
    try:
        choice = int(input("Enter entry number to delete: "))
        if 1 <= choice <= len(data):
            deleted = data.pop(choice-1)
            save_data(data)
            print(f"🗑️ Deleted entry: {deleted}")
        else:
            print("⚠️ Invalid number. No changes made.")
    except ValueError:
        print("⚠️ Please enter a valid number.")

def main():
    """Main loop with input validation"""
    while True:
        print("\n--- Menstrual Cycle Tracker ---")
        print("1. Add Cycle Entry")
        print("2. Predict Next Period")
        print("3. View Cycle History")
        print("4. Delete Entry")
        print("5. Exit")
        
        choice = input("Choose an option: ").strip()
        
        if choice == '1':
            date_input = input("Enter period start date (YYYY-MM-DD): ").strip()
            add_cycle_entry(date_input)
        elif choice == '2':
            predict_next_period()
        elif choice == '3':
            view_cycle_history()
        elif choice == '4':
            delete_cycle_entry()
        elif choice == '5':
            print("🌸 Goodbye! Take care!")
            break
        else:
            print("⚠️ Invalid choice. Try again.")

            
if __name__ == "__main__":
    main()
