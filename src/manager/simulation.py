from core.manager import *
from .train_simulate import TrainSimulator
from .terminal_simulate import TerminalSimulator
import json
from datetime import datetime


class Simulation:
    def __init__(self, manager: Manager, start_time: datetime):
        self.start_time = start_time
        self.manager = manager
        self.sim_trains: list[TrainSimulator] = []
        self.sim_terminals: list[TerminalSimulator] = []

    def get_road_by_name(self, name: str):
        for road in self.manager.roads:
            if road.name == name:
                return road
        assert False

    def step(self):
    def step():
        #        - берем и все переводим в час и расписывем весь путь и состояние поезда за каждый час, после 24 часов наступает новый день и все часы начинаются заново

        distance = self.road.distance
        speed = self.train.speed
        time_required_hours = distance / speed
        hours = int(time_required_hours)
        minutes = int((time_required_hours - hours) * 60)
        start_time = datetime(2021, 11, 1, 0, 0, 0)
        time_delta = timedelta(hours=hours, minutes=minutes) #
        end_time = start_time + time_delta
        time_train = end_time, self.train.name # запись
        return time_train
    
        pass

