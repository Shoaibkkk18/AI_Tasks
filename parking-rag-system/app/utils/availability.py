import pandas as pd
import os
import pandas as pd

# 1. Get the directory where availability.py lives
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

# 2. Build the absolute path to your data folder (going up 2 levels to root)
CSV_PATH = os.path.join(CURRENT_DIR, "..", "..", "data", "dynamic", "parking_dynamic.csv")

# 3. Read the CSV using the clean absolute path
dynamic_data = pd.read_csv(CSV_PATH)

dynamic_data = pd.read_csv(
    "data/dynamic/parking_dynamic.csv"
)


def check_availability(slot_type="Standard"):

    available = dynamic_data[
        dynamic_data["slot_type"] == slot_type
    ]["available_slots"].values[0]

    return available
