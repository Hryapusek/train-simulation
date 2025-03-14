from enum import Enum
from core.train import Train
from core.terminal import Terminal
from .simulation import Simulation
from datetime import datetime, timedelta

class TrainState(Enum):
    # Двигаемся
    MOVING = 1
    # Загружаемся
    LOADING = 2
    # Разгружаемся
    GIVEAWAY = 3
    # Ожидаем   
    WAITING = 4
class TrainSimulator:
    def __init__(self, train: Train, simulation: Simulation, terminal: Terminal):
        self.train = train
        self.simulation = simulation # здесь че
        self.state: TrainState = self.define_state()
        self.terminal = terminal


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

        # self.simulation.get_terminal_by_name(self.train.position["destination"]).free_space
    def define_state(self) -> TrainState:

        if self.train.position["traveled_dist"] not in (0, 2500, 4000):
            return TrainState.MOVING
        if self.terminal.stock_max == 0:
            if self.train.volume == self.train.capacity:
                return TrainState.MOVING
            else:
                return TrainState.WAITING if self.simulation.get_terminal_by_name(self.train.position["destination"]).free_space == 0 else TrainState.LOADING 
        if self.terminal.stock_max > 0:
            if self.train.volume == 0:
                return TrainState.MOVING
            else:
                return TrainState.WAITING if self.free_space == 0 else TrainState.GIVEAWAY


    def step(self) -> list[tuple[datetime, str, TrainState, int, str]]:
        train_list = []
        for train in self.simulation.trains: # здесь должны быть поезда
            distance = # подключить roads distance
            speed = train.speed
            time_required_hours = distance / speed
            hours = int(time_required_hours)
            minutes = int((time_required_hours - hours) * 60)
            start_time = datetime(2021, 11, 1, 0, 0, 0)
            time_delta = timedelta(hours=hours, minutes=minutes) 
            end_time = start_time + time_delta
            train_list.append((end_time, train.name, self.state, train.volume, train.position["destination"]))
        return train_list
        # создать список по каждому поезду и отправить в step в simulation

        # train_name = self.train.name
        # train_state = self.state
        # if train_state == TrainState.MOVING:
        #     data = self.step_moving()
        #     self.simulation.data.append(data)
        # elif train_state == TrainState.LOADING:
        #     self.step_loading()
        # elif train_state == TrainState.GIVEAWAY:
        #     self.step_giveaway()

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
        self.train.position["traveled_dist"] = min(self.train.position["traveled_dist"] + self.train.speed, self.simulation.get_road_by_name(self.train.road).distance)
        if self.train.position["traveled_dist"] == self.simulation.get_road_by_name(self.train.road).distance:
            terminal = self.simulation.get_terminal_by_name(self.train.position["destination"])
            if terminal and terminal.free_space > 0:
                if self.train.volume == 0:
                    self.state = TrainState.LOADING
                else:
                    self.state = TrainState.GIVEAWAY
            else:
                self.state = TrainState.WAITING

    def step_loading(self):
        # мы находимся на терминале и загружаемся - берем из терминала топливо
        terminal = self.simulation.get_terminal_by_name(self.train.position["destination"])
        if terminal and self.terminal.stock > 0:
            # беру столько топлива сколько могу (не более self.capacity)
            to_load = min(self.train.capacity - self.train.volume, terminal.stock)
            self.train.volume += to_load
            terminal.stock -= to_load
        """
        Обратиться к терминалу в котором мы сейчас находимся за топливом. 
        Необходимо проверить есть ли доступное топливо; 2 - терминалы сток и загрузка
        """
        pass

    def step_giveaway(self):
         # мы находимся на терминале и загружаемся - берем из терминала топливо
        terminal = self.simulation.get_terminal_by_name(self.train.position["destination"])
        if terminal and terminal.stock > 0:
            # беру столько топлива сколько могу (не более self.capacity)
            to_load = min(self.train.capacity - self.train.volume, terminal.stock)
            self.train.volume += to_load
            terminal.stock -= to_load
        """
        Аналогично предыдущему, но с выгрузкой топлива; 2  - терминалы сток и выгрузка
        """
        pass
