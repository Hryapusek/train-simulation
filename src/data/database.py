from __future__ import annotations
from .route_data import RouteData
from .terminal_data import TerminalData
from .transfer_point_data import TransferPointData
from .train_data import TrainData


class Database:
    def __init__(
        self,
        trains: list[TrainData],
        transfer_points: list[TransferPointData],
        terminals: list[TerminalData],
        routes: list[RouteData],
    ):
        self.trains = trains
        self.transfer_points = transfer_points
        self.terminals = terminals
        self.routes = routes

    def build_from_json(json_dict: dict) -> Database:
        trains = []
        transfer_points = []
        terminals = []
        routes = []

        for train_json in json_dict.get("trains", []):
            position = train_json.pop("position", {})
            # Inject nested values into the top-level dictionary
            train_json["target_station_name"] = position.get("destination")
            train_json["distance_travelled"] = position.get("traveled_dist")

            train = TrainData(**train_json)
            trains.append(train)

        for terminal_json in json_dict["stations"]["terminals"]:
            terminal = TerminalData(**terminal_json)
            terminals.append(terminal)

        for transfer_point_json in json_dict["stations"]["transfer_points"]:
            transfer_point = TransferPointData(**transfer_point_json)
            transfer_points.append(transfer_point)

        for route_json in json_dict.get("roads", []):
            route = RouteData(**route_json)
            routes.append(route)

        return Database(trains, transfer_points, terminals, routes)
