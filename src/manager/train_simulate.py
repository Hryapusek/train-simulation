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
        train_name = self.train.name
        train_state = self.state
        if train_state == TrainState.MOVING:
            data = self.step_moving()
            self.simulation.data.append(data)
        elif train_state == TrainState.LOADING:
            self.step_loading()
        elif train_state == TrainState.GIVEAWAY:
            self.step_giveaway()

    def step_moving(self):
        """
        Здесь мы двигаем поезд вперед
        и если надо обращаемся к другим состояниям
        """
        # Найти дорогу по которой мы сейчас двигаемся; 1 - traveled_dist
        # self.state = TrainState.GIVEAWAY (в  конце чекаем  волюм)
        distance = 2500 if self.train.road == "Raduzhney-Polyarny" else 4000
        if self.train.position["traveled_dist"] > 0:
            self.state = TrainState.MOVING
            time_required = self.train.position["traveled_dist"] / self.train.speed
            days = int(time_required)
            hours = int((time_required - days) * 24)
            minutes = int((time_required - days - hours / 24) * 1440)
            data = {
                "name": self.train.name,
                "datetime": datetime.now(),
                "time": f"{days} days, {hours} hours, {minutes} minutes",
                "state": self.state.name,
                "volume": self.train.volume,
                "road": self.train.road,
                "traveled_dist": self.train.position["traveled_dist"],
                "destination": self.train.position["destination"]
            }
            if self.train.position["traveled_dist"] == distance:
                self.state = TrainState.GIVEAWAY
                self.step_giveaway()
            elif self.train.position["traveled_dist"] == 0:
                if self.train.volume == 0:
                    self.state = TrainState.LOADING
                    self.step_loading()
        return data

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
