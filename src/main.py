from __future__ import annotations
from datetime import timedelta
from core.manager import Manager
from simulation.simulation import Simulation
import json

def read_database():
    INPUT_JSON_FILE_PATH = "input_train_sim.json"
    with open(INPUT_JSON_FILE_PATH, "r") as file:
        json_database = json.load(file)

    return Manager.from_json(json_database)

def main():
    manager: Manager = read_database()
    simulation = Simulation(manager)
    current_time = manager.other.datetime_start
    while current_time < manager.other.datetime_end:
        simulation.step()
        current_time += timedelta(hours=1)



if __name__ == "__main__":
    main()
