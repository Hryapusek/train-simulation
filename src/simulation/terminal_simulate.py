from core.terminal import Terminal
from enum import Enum
import numpy as np

class TerminalState(Enum):
    # Загружаем в терминал
    TAKE_FUEL = 1
    # Выгружаем в поезд
    GIVEAWAY_FUEL = 2

class TerminalSimulator:
    def __init__(self, terminal: Terminal, simulation):
        self.terminal = terminal
        self.simulation = simulation
        self.free_space = self.terminal.railways
        self.messages = [] #

    def generate_normal_distribution(self):
        mean = self.terminal.priduction['replenishment']
        std_dev = self.terminal.priduction['deviation']
        return np.random.normal(mean, std_dev)


    def step(self): # загрузка нефти
        pass
    def give_fuel(self, train) -> int:
        if self.terminal.stock >= train.volume:
            fuel_given = train.volume / self.terminal.loading_speed_train
            train.volume = 0
            self.terminal.stock -= fuel_given
            return TerminalState.GIVEAWAY_FUEL
        else:
            self.state = TerminalState.TAKE_FUEL
            return 0
    def take_fuel(self) -> int:
        train_volume = self.simulation.get_train_by_volume(self.terminal.capacity).train.volume
        generated_value = self.generate_normal_distribution()
        if self.terminal.stock < train_volume:
            train_volume / generated_value
                self.terminal.stock 
           
        else:
            self.state = TerminalState.WAITING
            return 0

    
    
    
        
    
