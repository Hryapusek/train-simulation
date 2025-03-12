from enum import Enum
from core.train import Train
from .simulation import Simulation


class TrainState(Enum):
    MOVING = 1
    # Загружаемся
    LOADING = 2
    # Разгружаемся
    GIVEAWAY = 3
    WAITING = 4
class TrainSimulator:
    def __init__(self, train: Train, simulation: Simulation):
        self.train = train
        self.simulation = simulation
        # TODO: определить состояние поезда
        self.state: TrainState = state


    def step(self):
        pass

    def step_moving(self):
        """
        Здесь мы двигаем поезд вперед
        и если надо обращаемся к другим состояниям
        """
        # Найти дорогу по которой мы сейчас двигаемся; 1 - traveled_dist
        # self.state = TrainState.GIVEAWAY (в  конце чекаем  волюм)
        self.simulation.manager.roads
        self.train.road
        self.train.position["traveled_dist"] += ...
        pass

    def step_loading(self):
        """
        Обратиться к терминалу в котором мы сейчас находимся за топливом. 
        Необходимо проверить есть ли доступное топливо; 2 - терминалы сток и загрузка
        """
        pass

    def step_giveaway(self):
        """
        Аналогично предыдущему, но с выгрузкой топлива; 2  - терминалы сток и выгрузка
        """
        pass
