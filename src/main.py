from __future__ import annotations
from datetime import datetime, timedelta  # Добавляем datetime для работы с датами
from data.database import Database
from simulation.simulation import Simulation
import json
from pathlib import Path
import os
import pandas as pd

# Get root directory (two levels up from src/main.py)
ROOT_DIR = Path(__file__).parent.parent

# Input/output directories
INPUT_JSON_FILE_PATH = ROOT_DIR / "input" / "input_train_sim.json"
OUTPUT_DIR = ROOT_DIR / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

def read_database():
    INPUT_JSON_FILE_PATH = Path(__file__).parent.parent / "input" / "input_train_sim.json"
    with open(INPUT_JSON_FILE_PATH, "r") as file:
        json_database = json.load(file)

    return Database.build_from_json(json_database)

def main(): 
    database = read_database()
    simulation = Simulation(database)
    
    current_time = datetime.strptime(database.other.datetime_start, "%d/%m/%Y %H:%M:%S")
    end_time = datetime.strptime(database.other.datetime_end, "%d/%m/%Y %H:%M:%S")
    
    while current_time < end_time:  
        simulation.current_time = current_time 
        simulation.simulate_step()
        current_time += timedelta(hours=1)

    # Handle terminals
    terminals_df = pd.DataFrame(simulation.terminal_logs)
    for station_name, group_df in terminals_df.groupby("station_name"):
        safe_name = station_name.replace(" ", "_").lower()
        file_path = OUTPUT_DIR / f"terminal_{safe_name}_log.csv"

        group_df = group_df[[
            "datetime", "stock", "extraction_amount", "train_on_track", "amount_loaded", "trains_queue"
        ]]

        # Round all float columns to 2 decimal places
        group_df = group_df.round(2)

        group_df.to_csv(file_path, index=False, encoding="utf-8-sig")

    # Handle transfer points
    transfer_df = pd.DataFrame(simulation.transfer_logs)
    for station_name, group_df in transfer_df.groupby("station_name"):
        safe_name = station_name.replace(" ", "_").lower()
        file_path = OUTPUT_DIR / f"transfer_point_{safe_name}_log.csv"

        group_df = group_df[[
            "datetime", "stock", "amount_loaded", "train_on_reserved_track",
            "train_on_track_1", "train_on_track_2", "amount_unloaded", "trains_queue"
        ]]

        # Round all float columns to 2 decimal places
        group_df = group_df.round(2)

        group_df.to_csv(file_path, index=False, encoding="utf-8-sig")


    # Print preview (optional)
    """ # print("=== Terminal Log ===")
    # print(terminals_df.to_markdown(tablefmt="grid"))

    # print("=== Transfer Point Log ===")
    # print(transfer_df.to_markdown(tablefmt="grid"))""" 

if __name__ == "__main__":
    main()