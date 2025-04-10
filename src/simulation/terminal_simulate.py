from .event import Event
from core.terminal import Terminal
from .train_simulate import TrainSimulator
from core.train import Train
import numpy as np 


class TerminalSimulator:

    def __init__(self, terminal: Terminal, simulation):
        self.terminal = terminal
        self.simulation = simulation
        self.free_space = self.terminal.railways

    def generate_normal_distribution(self):
        mean = self.terminal.production['replenishment']
        std_dev = self.terminal.production['deviation']
        return np.random.normal(mean, std_dev)


    def step(self): 
        pass
    
    def give_fuel(self, train) -> int:
        """
        Проверить есть ли доступная для выдачи нефть в терминале
        Если есть - выдать нефть поезду (return какое-то количество нефти)
        Зафиксировать событие
        """
        self.events.append(Event(
            date=self.simulation.time,
            oil_left=self.terminal.stock,
            oil_added=train.volume
        ))
        if self.terminal.stock >= train.volume:
            fuel_given = train.volume / self.terminal.loading_speed_train
            train.volume = 0
            self.terminal.stock -= fuel_given
            events_oil_left = Event(self.simulation.time, self.terminal.stock, None)
            return events_oil_left
        else:
            return 0
        
    def take_fuel(self, train: TrainSimulator):

        """
        Проверить сколько в терминале места для нефти.
        Если терминал полный - ничего не делаем. 
        Выгрузить с поезда нефть в соответствии с unloading_speed_train
        Зафиксировать событие выгрузки
        """
        self.events.append(Event(
            date=self.simulation.time,
            oil_left=self.terminal.stock,
            oil_added=self.train.volume
        ))

        name_terminal = self.simulation.get_terminal_by_name(self.train.name)
        train_volume = self.simulation.get_train_by_volume(self.terminal.volume)
        generated_value = self.generate_normal_distribution()
        if self.terminal.stock < train_volume:
            while self.terminal.stock < train_volume or name_terminal.free_space == 0:
                self.terminal.stock += generated_value
                train_volume -= generated_value
                events_oil_added = Event(self.simulation.time, None, self.terminal.stock)

            return events_oil_added
        
    def calculate_free_space(self):
        self.trains = []
        for train in self.simulation.manager.trains:
            state = train.define_state()
            self.trains.append({'name': train.name, 'state': state})
        with open('train.Train', 'r') as file:
            for line in file:
                name, state = line.strip().split(',')
                self.trains.append({'name': name, 'state': Train[state]})
        for train in self.trains:
            if train['state'] == Train.LOADING and train['position[destination]'] == 'Raduzhney':
                while self.free_space != self.simulation.get_terminal_by_name('Raduzhney').railways:
                    self.free_space += 1
        for train in self.trains:
            if train['state'] == Train.LOADING and train['position[destination]'] == 'Zvezda':
                while self.free_space != self.simulation.get_terminal_by_name('Zvezda').railways:
                    self.free_space += 1
        for train in self.trains:
            if train['state'] == Train.GIVEAWAY and train['name'] == "trainsFinish":
                self.free_space += 1
            else:   
                while self.free_space <= self.simulation.get_terminal_by_name("Polyarny").railways:
                    self.free_space += 1
            
                 

