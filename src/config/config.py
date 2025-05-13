import json
from datetime import datetime
from pathlib import Path


class Config:
    def __init__(self):
        self.input_file_path: Path = None
        self.output_dir: Path = None
        self.datetime_start: datetime = None
        self.datetime_end: datetime = None

    def from_json(file_path: str):
        result = __class__()
        with open(file_path, "r") as file:
            config = json.load(file)
        
        result.input_file_path = Path(config["input_file_path"])
        result.output_dir = Path(config["output_dir"])
        result.datetime_start = datetime.strptime(config["datetime_start"], "%d.%m.%Y %H:%M:%S")
        result.datetime_end = datetime.strptime(config["datetime_end"], "%d.%m.%Y %H:%M:%S")
        
        return result


_config: Config = None

def get_config() -> Config:
    global _config
    if _config is None:
        _config = Config.from_json("config/config.json")
    return _config
