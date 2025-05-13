from datetime import datetime, timedelta  # Добавляем datetime для работы с датами

import json
import pandas as pd

from data.database import Database
from simulation.simulation import Simulation
from config import config
from export_report import export_to_excel


def read_database() -> Database:
    with open(config.get_config().input_file_path, "r") as file:
        json_database = json.load(file)

    return Database.build_from_json(json_database)


def main():
    database = read_database()
    simulation = Simulation(database)
    
    current_time = config.get_config().datetime_start
    end_time = config.get_config().datetime_end
    total_duration = (end_time - config.get_config().datetime_start).total_seconds()

    while current_time < end_time:  
        simulation.current_time = current_time 
        simulation.simulate_step()
        current_time += timedelta(hours=1)

        elapsed_duration = (current_time - config.get_config().datetime_start).total_seconds()
        progress_percent = (elapsed_duration / total_duration) * 100
        print(" " * 50, end='\r', flush=True)
        arrow = '-' * int(progress_percent // 2) + ' ' * int(50 - progress_percent // 2)
        print(f"Simulation progress: [{arrow}] {progress_percent:.2f}%", end='\r', flush=True)
    print()


    # Handle terminals
    terminals_df = pd.DataFrame(simulation.terminal_logs)
    for station_name, group_df in terminals_df.groupby("station_name"):
        safe_name = station_name.replace(" ", "_").lower()
        file_path = config.get_config().output_dir / f"terminal_{safe_name}_log.csv"

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
        file_path = config.get_config().output_dir / f"transfer_point_{safe_name}_log.csv"

        group_df = group_df[[
            "datetime", "stock", "amount_loaded", "train_on_reserved_track",
            "train_on_track_1", "train_on_track_2", "amount_unloaded", "trains_queue", "track_status"
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
    export_to_excel()
    