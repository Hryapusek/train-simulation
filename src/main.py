from __future__ import annotations
from modules.initialize import from_json
import json

def read_database():
    INPUT_JSON_FILE_PATH = "input_train_sim.json"
    with open(INPUT_JSON_FILE_PATH, "r") as file:
        json_database = json.load(file)

    return from_json(json_database)

def main():
    database = read_database()
    for train in database.trains:
        


if __name__ == "__main__":
    main()

    