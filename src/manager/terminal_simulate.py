from enum import Enum
from core.terminal import Terminal
from core.train import Train
from .simulation import Simulation

class TerminalSimulator:
    def __init__(self, terminal: Terminal, simulation: Simulation):
        self.terminal = terminal
        self.simulation = simulation
        self.free_space = self.terminal.railways
        self.messages = []

    def step(self): # загрузка нефти
        pass

    def take_fuel(self) -> int:
        # сообщение о том что произошла выгрузка топлива
        return 50
