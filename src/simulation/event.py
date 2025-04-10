from datetime import datetime
from simulation.terminal_simulate import TerminalSimulator

class Event: # хранение данных из терминала
    def __init__(self, date: datetime, oil_left: int, oil_added: int, train_volume: int):
        self.date = date
        self.oil_left = oil_left
        self.oil_added = oil_added

class Data_Events:
    def __init__(self, ):
        pass

    def oil_left(self, events_oil_left) -> int:
        # берет инф из give_fuel  (events_oil_left) и хранит 
        # с временем для выводв в конечном результате
        pass

    def oil_added(self, events_oil_added) -> int:
     # берет инф из take_fuel  (events_oil_added) и хранит 
     # с временем для выводв в конечном результате

        pass
