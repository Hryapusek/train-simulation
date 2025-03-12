from enum import Enum
from core.train import Train


class TrainState(Enum):
    MOVING = 1
    # Загружаемся
    LOADING = 2
    # Разгружаемся
    GIVEAWAY = 3

class TrainSimulator:
    def __init__(self, train: Train, state: TrainState):
        self.train = train
        self.state: TrainState = state


    def step():
        pass
