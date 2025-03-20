from datetime import datetime, timedelta
from modules.initialize import from_json
import json

INPUT_JSON_FILE_PATH = "input_train_sim.json"
with open(INPUT_JSON_FILE_PATH, "r") as file:
    json_database = json.load(file)
data = from_json(json_database)

# function (road Raduzhney-Polyarny)
def go_away(distance, speed):
    for train in data["trains"]:
        # distance = {roads.distance}  # подключить roads distance
        distance = self.road.distance
        speed = self.train.speed
        time_required_hours = distance / speed
        hours = int(time_required_hours)
        minutes = int((time_required_hours - hours) * 60)
        start_time = datetime(2021, 11, 1, 0, 0, 0)
        time_delta = timedelta(hours=hours, minutes=minutes) #
        end_time = start_time + time_delta
        time_train = end_time, self.train.name # запись
        return time_train
print (go_away())
    


______
# 1
#  manager 
#   for train_json in json_dict.get("trains", []):
#             train = Train(**train_json)
#             trains.append(train) # 
# 2
# train 
# if __name__ == "__main__": #
#     train1 = Train(name="trainRP1", speed=40, capacity=4000, road="Raduzhney-Polyarny", volume=4000, position={"destination": "Polyarny", "traveled_dist": 1250})
#     train2 = Train(name="trainRP2", speed=40, capacity=4000, road="Raduzhney-Polyarny", volume=0, position={"destination": "Polyarny", "traveled_dist": 2500})
# 3
# initilize ? 
# 4 
# simulatoin 
# self.sim_terminals: list[TerminalSimulator] = [] " убираю скобки "
# 5
# simulation
# self.state: TrainState = self.define_state() 
# define_state ?
# 6
# terminal_simulatetion
#  self.messages = [] ?
_______

class Terminal:
    def init(self, name):
        self.name = name
        self.state = "idle"  # Пример состояния (можно адаптировать под свои нужды)
    
    def step(self, time):
        # Логика изменения состояния терминала за время time
        print(f"Терминал {self.name} шаг: состояние {self.state} за время {time}")
        # Обновление состояния, например, работа терминала:
        if self.state == "idle":
            self.state = "working"
        elif self.state == "working":
            self.state = "idle"
        else:
            self.state = "idle"


class Train:
    def init(self, name, position):
        self.name = name
        self.position = position  # Позиция поезда в системе
    
    def step(self, time):
        # Логика перемещения поезда за время time
        print(f"Поезд {self.name} перемещается на {time} единиц времени.")
        self.position += time  # Пример движения поезда на величину времени


class Simulator:
    def init(self):
        self.terminals = []  # Список терминалов
        self.trains = []  # Список поездов
    
    def add_terminal(self, terminal):
        self.terminals.append(terminal)
    
    def add_train(self, train):
        self.trains.append(train)
    
    def simulate_step(self, time):
        # Сначала шаг для всех терминалов
        for terminal in self.terminals:
            terminal.step(time)
        
        # Затем шаг для всех поездов
        for train in self.trains:
            train.step(time)
    

# Создаем объекты
terminal1 = Terminal("T1")
terminal2 = Terminal("T2")
train1 = Train("Train1", 0)
train2 = Train("Train2", 5)

# Создаем симулятор и добавляем терминалы и поезда
simulator = Simulator()
simulator.add_terminal(terminal1)
simulator.add_terminal(terminal2)
simulator.add_train(train1)
simulator.add_train(train2)

# Симулируем шаг системы за 10 единиц времени
simulator.simulate_step(10)

______________

import numpy as np

def generate_normal_distribution(mean=150, std_dev=10):
    return np.random.normal(mean, std_dev)

# Пример использования
generated_value = generate_normal_distribution()
print(generated_value)