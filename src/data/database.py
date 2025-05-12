from __future__ import annotations
from .other_data import OtherData
from .route_data import RouteData
from .station_data import StationData
from .train_data import TrainData


class Database:
    def __init__(self, trains: list[TrainData], stations: list[StationData], routes: list[RouteData], other: OtherData):
        self.trains = trains
        self.stations = stations
        self.routes = routes
        self.other = other

    def build_from_json(json_dict: dict) -> Database:
        trains = []
        stations = []
        routes = []  

        for train_json in json_dict.get("trains", []):
            position = train_json.pop("position", {})
            # Inject nested values into the top-level dictionary
            train_json["target_station_name"] = position.get("destination")
            train_json["distance_travelled"] = position.get("traveled_dist")
            
            train = TrainData(**train_json)
            trains.append(train)

        for station_json in json_dict.get("terminals", []):
            station = StationData(**station_json)
            stations.append(station)

        for route_json in json_dict.get("roads", []):
            route = RouteData(**route_json)
            routes.append(route)

        other = OtherData(**json_dict.get("other", {}))
        return Database(trains, stations, routes, other)
