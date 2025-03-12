from enum import Enum
from core.train import Train
from .simulation import Simulation

class TerminalSimulator:
    def __init__(self, terminal: Terminal, simulation: Simulation):
        self.terminal = terminal
        self.simulation = simulation
    pass

    def step(self): # загрузка нефти
            pass