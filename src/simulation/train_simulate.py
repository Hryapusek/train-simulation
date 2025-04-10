from __future__ import annotations
from core.train import Train, TrainState
from datetime import datetime

# TODO: comment me otherwise you will get error
from simulation.simulation import Simulation

class TrainSimulator:
    def __init__(self, train: Train, simulation: Simulation, state: TrainState):
        self.train = train
        self.simulation = simulation
        self.state = state
        self.train.position 

    def step(self):
        # создать список по каждому поезду и отправить в step в simulation
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

        name_terminal = self.simulation.get_terminal_by_name(self.train.name)
        self.train.position["traveled_dist"] = min(self.train.position["traveled_dist"] + self.train.speed, self.simulation.get_road_by_name(self.train.road).distance)
        if self.train.position["traveled_dist"] == self.simulation.get_road_by_name(self.train.road).distance:
            terminal = self.simulation.get_terminal_by_name(self.train.position["destination"])
            if terminal and name_terminal.free_space > 0:
                if self.train.volume == 0:
                    self.state = TrainState.LOADING
                else:
                    self.state = TrainState.GIVEAWAY
            else:
                self.state = TrainState.WAITING

    def step_loading(self):
        # мы находимся на терминале и загружаемся - берем из терминала топливо
        terminal = self.simulation.get_terminal_by_name(self.train.position["destination"])
        self.train.volume += terminal.give_fuel(self)

        """
        Обратиться к терминалу в котором мы сейчас находимся за топливом. 
        Необходимо проверить есть ли доступное топливо; 2 - терминалы сток и загрузка
        """
        pass

    def step_giveaway(self):
         # мы находимся на терминале и загружаемся - берем из терминала топливо
        terminal = self.simulation.get_terminal_by_name(self.train.position["destination"])
        terminal.take_fuel(self)
        """
        Аналогично предыдущему, но с выгрузкой топлива; 2  - терминалы сток и выгрузка
        """
        pass

    def reset_position_and_destination(self):
        if self.train.position["traveled_dist"] == self.simulation.get_road_by_name(self.train.road).distance and self.train.volume == 0:
            self.train.position["traveled_dist"] = 0
            if self.train.position["destination"] == "Polyarny":
                self.train.position["destination"] = "Raduzhney"
            else:
                self.train.position["destination"] = "Polyarny"
