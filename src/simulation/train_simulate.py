from enum import Enum
from core.train import Train
from datetime import datetime

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
    def __init__(self, train: Train, simulation):
        self.train = train
        self.simulation = simulation
        self.state: TrainState = self.define_state() #


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
    
    

    def define_state(self) -> TrainState:
        train_road = self.simulation.get_road_by_name(self.train.road)
        name_terminal = self.simulation.get_terminal_by_name(self.train.name)
        # MOVING
        if self.train.position["traveled_dist"] != train_road.distance or 0:
            return TrainState.MOVING
        
        if self.train.position["traveled_dist"] == 0 and self.train.volume == self.train.capacity:
            return TrainState.MOVING
        
        if self.train.position["traveled_dist"] == train_road.distance and self.train.volume == 0:
            return TrainState.MOVING
        # LOADING
        if self.train.position["traveled_dist"]  == 0 and self.train.volume != self.train.capacity:
            if name_terminal.free_space == 0:
                return TrainState.LOADING
            else:
                return TrainState.WAITING
        # GIVEAWAY  
        if self.train.position["traveled_dist"] == train_road.distance and self.train.volume == self.train.capacity:
            if name_terminal.free_space == 0:
                return TrainState.GIVEAWAY
            else:
                
    def step(self) -> list[tuple[datetime, str, TrainState, int, str]]:
        # создать список по каждому поезду и отправить в step в simulation

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
    def reset_position_and_destination(self):
        if self.train.position["traveled_dist"] == self.simulation.get_road_by_name(self.train.road).distance and self.train.volume == 0:
            self.train.position["traveled_dist"] = 0
            if self.train.position["destination"] == "Polyarny":
                self.train.position["destination"] = "Raduzhney"
            else:
                self.train.position["destination"] = "Polyarny"
