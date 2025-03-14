from core.manager import *
from .train_simulate import TrainSimulator
from .terminal_simulate import TerminalSimulator
import json
from datetime import datetime, timedelta


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

    def get_terminal_by_name(self, name: str) -> TerminalSimulator:
        for terminal in self.sim_terminals:
            if terminal.terminal.name == name:
                return terminal
        assert False

    def step(self):
        for train in self.manager.trains:
            road = self.get_road_by_name(train.road)
            distance = road.distance
            speed = train.speed
            time_required_hours = distance / speed
            hours = int(time_required_hours)
            minutes = int((time_required_hours - hours) * 60)
            start_time = self.start_time
            time_delta = timedelta(hours=hours, minutes=minutes)
            end_time = start_time + time_delta
            time_train = (end_time, train.name)
            print(time_train)  # or store the result as needed

        for simulator in self.sim_trains + self.sim_terminals:
            simulator.step()

