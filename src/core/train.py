from pydantic import BaseModel
from enum import Enum
from simulation.simulation import Simulation

class TrainModel(BaseModel):
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

class Train:
    def __init__(self, train: TrainModel, simulation: Simulation):
        self.name = train.name
        self.speed = train.speed
        self.capacity = train.capacity
        self.road = train.road
        self.volume = train.volume
        self.position = train.position
        self.simulation = simulation

    def define_state(self):
        train_road = self.simulation.get_road_by_name(self.road)
        name_terminal = self.simulation.get_terminal_by_name(self.name)
        if self.position["traveled_dist"] != train_road.distance:
            return TrainState.MOVING
        if self.position["traveled_dist"] == 0 and self.volume == self.capacity:
            return TrainState.MOVING
        if self.position["traveled_dist"] == train_road.distance and self.volume == 0:
            return TrainState.MOVING
        if self.position["traveled_dist"] == 0 and self.volume != self.capacity:
            if name_terminal.free_space == 0:
                return TrainState.LOADING
            else:
                return TrainState.WAITING
        if self.position["traveled_dist"] == train_road.distance and self.volume == self.capacity:
            if name_terminal.free_space == 0:
                return TrainState.GIVEAWAY
            else:
                return TrainState.WAITING
