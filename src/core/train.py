from pydantic import BaseModel
from enum import Enum
from simulation.simulation import Simulation

class Train(BaseModel):
    name: str
    speed: int | None = None
    capacity: int
    road: str
    volume: int
    position: dict


class TrainState(Enum):
    # Двигаемся
    MOVING = 1
    # Загружаемся
    LOADING = 2
    # Разгружаемся
    GIVEAWAY = 3
    # Ожидаем   
    WAITING = 4


class Train_Model:
    def __init__(self, train: Train, simulation: Simulation):
        self.train = train
        self.simulation = simulation
        self.train.position 

    def define_state(self):
            train_road = self.simulation.get_road_by_name(self.train.road)
            name_terminal = self.simulation.get_terminal_by_name(self.train.name)
            # MOVING
            if self.train.position["traveled_dist"] != train_road.distance or 0:
                return TrainState.MOVING
            
            if self.train.position["traveled_dist"] == 0 and self.train.volume == self.train.capacity:
                return TrainState.MOVING
            
            if self.train.position["traveled_dist"] == train_road.distance and self.train.volume == 0:
                return TrainState.MOVING
            # LOADING
            if self.train.position["traveled_dist"]  == 0 and self.train.volume != self.train.capacity:
                if name_terminal.free_space == 0:
                    return TrainState.LOADING
                else:
                    return TrainState.WAITING
            # GIVEAWAY  
            if self.train.position["traveled_dist"] == train_road.distance and self.train.volume == self.train.capacity:
                if name_terminal.free_space == 0:
                    return TrainState.GIVEAWAY
                else:
                    pass