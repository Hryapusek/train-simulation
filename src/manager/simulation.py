from core.manager import *
from .train_simulate import TrainSimulator
from .terminal_simulate import TerminalSimulator

class Simulation:
    def __init__(self, manager: Manager):
        self.manager = []
        self.sim_trains = []
        self.sim_terminals = []

    def get_terminal(name: str) -> TerminalSimulator:
        pass

    def step():
        pass
