import json
from pathlib import Path

class Config:
    def __init__(self, input_file_path: str, output_dir: str):
        self.input_file_path = Path(input_file_path)
        self.output_dir = Path(output_dir)

    def from_json(file_path: str):
        with open(file_path, "r") as file:
            config = json.load(file)
        return __class__(config["input_file_path"], config["output_dir"])


def get_config() -> Config:
    return Config.from_json("config/config.json")
