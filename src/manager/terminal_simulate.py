from enum import Enum
from core.terminal import Terminal
from core.train import Train
from .simulation import Simulation

class TerminalSimulator:
    def __init__(self, terminal: Terminal, simulation: Simulation):
        self.terminal = terminal
        self.simulation = simulation
        self.free_space = self.terminal.railways
        self.messages = [] # эт че

    def step(self): # загрузка нефти
        timestamp = self.simulation.current_time
        event = {
            "timestamp": timestamp,
            "terminal": self.terminal.name,
            "stock": self.terminal.stock,
            "production": self.terminal.production["replenishment"],
            "unloaded": 0
        }
        if self.terminal.production.replenishment > 0:
            self.terminal.stock += self.terminal.production.replenishment
            event["unloaded"] = self.terminal.production.replenishment
        self.messages.append(event)

    def take_fuel(self) -> int:
        event = {
            "timestamp": self.simulation.current_time,
            "terminal": self.terminal.name,
            "stock": self.terminal.stock,
            "production": self.terminal.production["replenishment"],
            "unloaded": 0
        }
        if self.terminal.production.replenishment > 0:
            self.terminal.stock += self.terminal.production.replenishment
            event["unloaded"] = self.terminal.production.replenishment
        self.messages.append(event)
        return 50
    
    def give_fuel(self) -> int:
        
    
