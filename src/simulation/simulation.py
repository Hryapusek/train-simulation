from core.manager import *
from .train_simulate import TrainSimulator
from .terminal_simulate import TerminalSimulator
from datetime import timedelta


class Simulation:
    def __init__(self, manager: Manager):
        self.manager = manager
        self.sim_trains: list[TrainSimulator] = []
        self.sim_terminals: list[TerminalSimulator] = []
        self.lfkajldsf
        for train in self.manager.trains:
            new_simulation_train = TrainSimulator(train, self)
            self.sim_trains.append(new_simulation_train)

        for terminal in self.manager.terminals:
            new_simulation_terminal = TerminalSimulator(terminal, self)
            self.sim_terminals.append(new_simulation_terminal)
        # Пройтись фором по всем поездам из manager 
        # и на основе их создать объекты TrainSimulator
        # и сложить их в список self.sim_trains


    def get_terminal_by_name(self, name: str) -> TerminalSimulator:
        for terminal in self.sim_terminals:
            if terminal.terminal.name == name:
                return terminal
        assert False

    def get_road_by_name(self, name: str) -> Road:
        for road in self.manager.roads:
            if road.name == name:
                return road
        assert False
    # добавила для сравнения volume и stock
    def get_train_by_volume(self, volume: int) -> TrainSimulator:
        for train in self.sim_trains:
            if train.train.volume == volume:
                return train
        assert False

    def simulate_step(self):
        # Сначала шаг для всех терминалов
        for terminal in self.sim_terminals:
            terminal.step()
        
        # Затем шаг для всех поездов
        for train in self.sim_trains:
            train.step()

        """
        Эта функция делает шаг всей системы. То есть она симулирует работу системы за указанное время.
        Симуляция состоит из поездов и терминалов. Мы должны по очереди - сначала все терминалы,
        потом все поезда подвинуть на указанное время вперед. Мы договорились что во всех них есть функция step()
        которая делает в объекте действия за указанное время.
        """
        

