from core.manager import *
from .train_simulate import TrainSimulator
from .terminal_simulate import TerminalSimulator

class Simulation:
    def __init__(self, manager: Manager):
        self.manager = manager
        self.sim_trains: list[TrainSimulator] = []
        self.sim_terminals: list[TerminalSimulator] = []

    def step():
        """
            Здесь необходимо вызывать по очереди методы step во всех
            - Терминалах
            - Поездах
        """
        pass
