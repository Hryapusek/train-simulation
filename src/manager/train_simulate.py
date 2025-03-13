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
        """
        1. Если мы не находимся в конце дороги и не в начале - значит мы в движении
        2. Если мы на терминале и терминал типа загрузка - проверяем заполнен ли поезд
            - Если поезд заполнен - мы в движении
            - Если поезд не заполнен и в терминале ЕСТЬ место - мы в состоянии загрузки
            - Иначе мы в состоянии ожидания railways
        3. Если мы на терминале и терминал типа выгрузка - проверяем выгружен ли поезд
            - Если поезд выгружен - мы в движении
            - Если поезд не выгружен и в терминале ЕСТЬ место - мы в состоянии выгрузки
            - Иначе мы в состоянии ожидания railways
        """
        if self.train.volume > 0 and self.train.position["traveled_dist"] >= 0:
            return TrainState.MOVING
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
        Здесь мы просто двигаем поезд вперед на self.speed
        При этом надо проверить вдруг мы приехали чтобы не выйти за пределы дороги

        Если мы приехали - необходимо проверить есть ли в терминале свободное место
        Если нету - переходим в состояние ожидания места
        Если есть - проверяем в какой терминал приехали
            - Если поезд пустой,
                то переходим в состояние загрузки
            - Иначе переходим в состояние выгрузки
        """
        # Найти дорогу по которой мы сейчас двигаемся; 1 - traveled_dist
        # self.state = TrainState.GIVEAWAY (в  конце чекаем  волюм)
        # Здесь нужно подвинуть поезд но не выйти за пределы дороги
        distance = self.simulation.get_road_by_name(self.train.road).distance
        if self.train.position["traveled_dist"] == distance:
            # В зависимости от терминала - переходим в состояние загрузки или разгрузки
            self.state = TrainState.GIVEAWAY
            self.step_giveaway()
        elif self.train.position["traveled_dist"] == 0:
            # Аналогично
            if self.train.volume == 0:
                self.state = TrainState.LOADING
                self.step_loading()

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
