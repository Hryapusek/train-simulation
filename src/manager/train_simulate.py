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
        self.state: TrainState = self.define_state()

    def define_state(self) -> TrainState:
        if self.train.volume > 0 and self.train.position["traveled_dist"] > 0:
            return TrainState.MOVING
        elif self.train.volume > 0 and self.train.position["traveled_dist"] < 0:
            return TrainState.LOADING
        elif self.train.volume == 0 and self.train.road == "Raduzhney-Polyarny" and self.train.position["traveled_dist"] == 2500:
            return TrainState.GIVEAWAY
        elif self.train.volume == 0 and self.train.road == "Zvezda-Polyarny" and self.train.position["traveled_dist"] == 4000:
            return TrainState.GIVEAWAY
        elif self.train.volume == 0 and self.train.position["traveled_dist"] == 0:
            return TrainState.WAITING



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
