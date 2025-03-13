from core.manager import *
from .train_simulate import TrainSimulator
from .terminal_simulate import TerminalSimulator
import json
from datetime import datetime


class Simulation:
    def __init__(self, manager: Manager):
        self.manager = manager
        self.sim_trains: list[TrainSimulator] = []
        self.sim_terminals: list[TerminalSimulator] = []

    def step(self):
    def step():
        """
            Здесь необходимо вызывать по очереди методы step во всех
            - Терминалах
            - Поездах
        """
        data = {
            "время и дата": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Название поезда": "",
            "Состояние поезда": "",
            "Остаток нефти в поезде": 0,
            "Пункт назначения поезда": "",
            "Название терминала": "",
            "Остаток нефти в терминале": 0,
            "Поезд в терминале": ""
        }

        for train_sim in self.sim_trains:
            train_sim.step()

        pass

