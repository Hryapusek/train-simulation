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

    def __init__(self, name, speed, capacity, road, volume, position, simulation: Simulation):
        self.TrainModel.name = name
        self.TrainModel.speed = speed
        self.TrainModel.capacity = capacity
        self.TrainModel.road = road
        self.TrainModel.volume = volume
        self.TrainModel.position = {
            "destination": position[0],
            "traveled_dist": position[1]
        }
        self.simulation = simulation

    def define_state(self):
        train_road = self.simulation.get_road_by_name(self.road)
        name_terminal = self.simulation.get_terminal_by_name(self.TrainModel.name)
        if self.TrainModel.position["traveled_dist"] != train_road.distance or 0:
            return TrainState.MOVING
        if self.TrainModel.position["traveled_dist"] == 0 and self.TrainModel.volume == self.TrainModel.capacity:
            return TrainState.MOVING
        if self.TrainModel.position["traveled_dist"] == train_road.distance and self.TrainModel.volume == 0:
            return TrainState.MOVING
        if self.TrainModel.position["traveled_dist"]  == 0 and self.TrainModel.volume != self.TrainModel.capacity:
            if name_terminal.free_space == 0:
                return TrainState.LOADING
            else:
                return TrainState.WAITING
        if self.TrainModel.position["traveled_dist"] == train_road.distance and self.TrainModel.volume == self.TrainModel.capacity:
            if name_terminal.free_space == 0:
                return TrainState.GIVEAWAY
            else:
                pass
