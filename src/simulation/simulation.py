from core.manager import *
from .train_simulate import TrainSimulator
from .terminal_simulate import TerminalSimulator
from datetime import timedelta


class Simulation:
    def __init__(self, manager: Manager):
        self.manager = manager
        self.sim_trains: list[TrainSimulator] = []
        self.sim_terminals: list[TerminalSimulator] = []

        for train in self.manager.trains:
            new_simulation_train = TrainSimulator(train, self)
            self.sim_trains.append(new_simulation_train)

        for terminal in self.manager.terminals:
            new_simulation_terminal = TerminalSimulator(terminal, self)
            self.sim_terminals.append(new_simulation_terminal)

        # Пройтись фором по всем поездам из manager 
        # и на основе их создать объекты TrainSimulator
        # и сложить их в список self.sim_trains
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

    def get_terminal_by_stock_max(self, stock_max: int) -> TerminalSimulator:

    def get_road_by_name(self, name: str) -> Road:
        for road in self.manager.roads:
            if road.name == name:
                return road
        assert False

    def step(self):
        """
        Эта функция делает шаг всей системы. То есть она симулирует работу системы за час.
        Симуляция состоит из поездов и терминалов. Мы должны по очереди - сначала все терминалы,
        потом все поезда подвинуть на час вперед. Мы договорились что во всех них есть функция step()
        которая делает в объекте действия за один час.
        """

        # Это не совсем корректно, так как система логирования будет выглядеть по другому
        

        for simulator in self.sim_terminals + self.sim_trains:
            simulator.step()

