from enum import Enum
from core.train import Train
from .simulation import Simulation


class TrainState(Enum):
    MOVING = 1
    # Загружаемся
    LOADING = 2
    # Разгружаемся
    GIVEAWAY = 3

class TrainSimulator:
    def __init__(self, train: Train, state: TrainState, simulation: Simulation):
        self.train = train
        self.state: TrainState = state
        self.simulation = simulation


    def step(self):
        pass

    def step_moving(self):
        """
        Здесь мы двигаем поезд вперед
        и если надо обращаемся к другим состояниям
        """
        # Найти дорогу по которой мы сейчас двигаемся
        self.simulation.manager.roads
        self.train.road
        self.train.position["traveled_dist"] += ...
        pass

    def step_loading(self):
        """
        Обратиться к терминалу в котором мы сейчас находимся за топливом. 
        Необходимо проверить есть ли доступное топливо
        """
        pass

    def step_giveaway(self):
        """
        Аналогично предыдущему, но с выгрузкой топлива
        """
        pass
