from data.database import *
from .train_simulator import TrainSimulator
from .station_simulator import StationSimulator
from .station_simulator import TerminalSimulator
from .station_simulator import TransferPointSimulator
from .station_simulator import TransferPointState
from .station_simulator import TerminalState
from .train_simulator import StationType
from datetime import timedelta, datetime


class Simulation:
    def __init__(self, database: Database):
        self.database = database

        self.transfer_point_simulators: list[TransferPointSimulator] = []
        self.terminal_simulators: list[TerminalSimulator] = []

        self.train_simulators: list[TrainSimulator] = []
        
        self.current_time = None
        
        self.terminal_logs = []
        self.transfer_logs = []

        for transfer_point in self.database.transfer_points:
            new_transfer_point_simulator = TransferPointSimulator(transfer_point, self)
            self.transfer_point_simulators.append(new_transfer_point_simulator)

        for terminal in self.database.terminals:
            new_terminal_simulator = TerminalSimulator(terminal, self)
            self.terminal_simulators.append(new_terminal_simulator)
            
        for train in self.database.trains:                               
            new_train_simulator = TrainSimulator(train, self)
            self.train_simulators.append(new_train_simulator)

    def get_station_with_type(self, name: str) -> tuple[object, str] | None:
        station: StationSimulator
        for station in self.transfer_point_simulators + self.terminal_simulators:
            if station.data.name == name:
                station_type = (
                    StationType.TRANSFER_POINT
                    if isinstance(station, TransferPointSimulator)
                    else StationType.TERMINAL
                )
                return station, station_type
        assert False

    def get_route_by_name(self, name: str) -> RouteData:
        for road in self.database.routes:
            if road.name == name:
                return road
        assert False

    def step(self):

        # шаг для всех поездов
        for train in self.train_simulators:
            train.simulate_step()

        # Step and log terminals
        for terminal in self.terminal_simulators:
            terminal.step()
            self.terminal_logs.append(self._log_terminal(terminal))



        # Step and log transfer points
        for tp in self.transfer_point_simulators:
            tp.step()
            self.transfer_logs.append(self._log_transfer_point(tp))
    
    def _log_terminal(self, terminal: TerminalSimulator):
        return {
            "datetime": self.current_time.strftime("%d-%m-%Y %H:%M:%S"),
            "station_type": "terminal",
            "station_name": terminal.data.name,
            "stock": terminal.data.stock,
            "extraction_amount": terminal.last_production_result if terminal.state == TerminalState.ACCUMULATING else None,
            "train_on_track": terminal.tracks_status[0].data.name + " | " + str(terminal.tracks_status[0].data.volume) if (len(terminal.tracks_status) > 0 and isinstance(terminal.tracks_status[0], TrainSimulator)) else None,
            "amount_loaded": terminal.count_trains_on_tracks() * terminal.data.loading_speed if terminal.state == TerminalState.DISTRIBUTING else None,
            "trains_queue": ", ".join(train.data.name for train in terminal.trains_queue) if terminal.trains_queue else "—"
        }

    def _log_transfer_point(self, tp: TransferPointSimulator):
        return {
            "datetime": self.current_time.strftime("%d-%m-%Y %H:%M:%S"),
            "station_type": "transfer_point",
            "station_name": tp.data.name,
            "stock": tp.data.stock,
            "amount_loaded": tp.data.loading_speed if tp.state == TransferPointState.DISTRIBUTING else None,
            "train_on_reserved_track": "trainsFinish" if tp.state == TransferPointState.DISTRIBUTING else None,                            
            "train_on_track_1": tp.tracks_status[0].data.name + " | " + str(tp.tracks_status[0].data.volume) if (len(tp.tracks_status) > 0 and isinstance(tp.tracks_status[0], TrainSimulator)) else None,
            "train_on_track_2": tp.tracks_status[1].data.name + " | " + str(tp.tracks_status[1].data.volume) if (len(tp.tracks_status) > 1 and isinstance(tp.tracks_status[1], TrainSimulator)) else None,
            "amount_unloaded": tp.count_trains_on_tracks() * tp.data.unloading_speed if tp.state == TransferPointState.ACCUMULATING else None,
            "trains_queue": ", ".join(train.data.name for train in tp.trains_queue) if tp.trains_queue else "—"
        }
