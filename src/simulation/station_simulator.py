from abc import ABC, abstractmethod

import numpy as np
from datetime import datetime
from enum import Enum, auto

from data.station_data import StationData
from .train_simulator import TrainSimulator
from .train_simulator import TrainState
from .train_simulator import StationType
from data.train_data import TrainData



class TransferPointState(Enum):
    ACCUMULATING = auto()  # GETTING      Unloading a train
    DISTRIBUTING = auto()  # GIVING       Loading a train
    IDLE = auto()  # WAITING FOR TRAINS


class TerminalState(Enum):
    ACCUMULATING = auto()  # GETTING      Mining oil
    DISTRIBUTING = auto()  # GIVING       Loading a train

class StationSimulator(ABC):
    def __init__(self, station_data: StationData, simulation):
        self.data = station_data
        self.parent_simulation = simulation
        self.tracks_status: list[TrainSimulator | None] = [None] * self.data.total_functional_tracks
        self.trains_queue: list[TrainSimulator] = []

    @abstractmethod
    def step(self):
        pass
    
    @abstractmethod
    def on_train_left(self, train):
        pass
    
    @abstractmethod
    def redefine_state(self):
        pass

    def add_train_to_queue(self, train: TrainSimulator):
        self.trains_queue.append(train)

    def add_train_to_track(self, train):
        for track_id, track_status in enumerate(self.tracks_status):
            if track_status is None:
                self.tracks_status[track_id] = train
                return

    def count_available_tracks(self):
        """Returns the number of available (empty) tracks."""
        return self.tracks_status.count(None)
    
    def count_trains_on_tracks(self):
        return len([t for t in self.tracks_status if isinstance(t, TrainSimulator)])

class TransferPointSimulator(StationSimulator):
    def __init__(self, station_data, simulation):
        StationSimulator.__init__(self, station_data, simulation)

        self.ghost_train_data = {}
        self.state = TransferPointState.IDLE

    def initialize_ghost_train(self, volume, capacity):
        self.ghost_train_data["volume"] = volume
        self.ghost_train_data["capacity"] = capacity

    def redefine_state(self):
        if self.state == TransferPointState.DISTRIBUTING:
            return
        self.state = TransferPointState.ACCUMULATING
              
    def take_fuel(self, train: TrainSimulator):
        if self.state == TransferPointState.DISTRIBUTING:
            return 0
        amount_to_take = self.data.unloading_speed
        self.data.stock += amount_to_take
        return amount_to_take

    def on_train_left(self, train):
        # Free the track first
        for track_id, track_status in enumerate(self.tracks_status):
            if track_status == train:
                self.tracks_status[track_id] = None
                break

        # Early exit if queue is empty
        if not self.trains_queue:
            return

        train_to_process: TrainSimulator = self.trains_queue.pop(0)
        self.add_train_to_track(train_to_process)
        self.state = TransferPointState.ACCUMULATING
        train_to_process.state = TrainState.UNLOADING

    def step(self):
        if (
            self.data.stock >= self.ghost_train_data["capacity"]
        ):
            self.state = TransferPointState.DISTRIBUTING

        if self.state == TransferPointState.DISTRIBUTING:
            left_to_load = (
                self.ghost_train_data["capacity"] - self.ghost_train_data["volume"]
            )

            if (
                left_to_load >= self.data.loading_speed
            ): 
                amount_to_load = self.data.loading_speed
            else:
                amount_to_load = left_to_load

            self.data.stock -= amount_to_load
            self.ghost_train_data["volume"] += amount_to_load

            if self.ghost_train_data["volume"] == self.ghost_train_data["capacity"]:
                self.state = TransferPointState.IDLE
                self.ghost_train_data["volume"] = 0 #reset the ghost train






      # if self.count_trains_on_tracks() > 0:
        #     self.state = TransferPointState.ACCUMULATING    
        # else:
        #     self.state = TransferPointState.IDLE
        
        
        
    # if self.state == TerminalState.ACCUMULATING:
        #     return      #accumulating will turn itself off when it finishes in the step() -> check_queue()
        
        # if self.count_trains_on_tracks() > 0:
        #     self.state = TerminalState.DISTRIBUTING







class TerminalSimulator(StationSimulator):
    def __init__(self, station_data, simulation):
        StationSimulator.__init__(self, station_data, simulation)
        self.state = TerminalState.ACCUMULATING
        
        self.last_production_result = None # FOR LOGS
        
    def generate_normal_distribution(self):
        mean = self.data.production["replenishment"]
        std_dev = self.data.production["deviation"]
        result =  np.random.normal(mean, std_dev)
        self.last_production_result = result
        return result
    
    def give_fuel(self, train) -> int:
        amount_to_give = self.data.loading_speed
        self.data.stock -= amount_to_give
        return amount_to_give

    def redefine_state(self):
        self.state = TerminalState.DISTRIBUTING
        
    def on_train_left(self, train):
        # Free the track first
        for track_id, track_status in enumerate(self.tracks_status):
            if track_status == train:
                self.tracks_status[track_id] = None
                break
        
        self.check_queue()

    def check_queue(self): 
        # Early exit if queue is empty
        if not self.trains_queue:
            self.state = TerminalState.ACCUMULATING
            return
        
        # Peek first without popping
        train_to_process: TrainSimulator = self.trains_queue[0]

        if self.data.stock >= train_to_process.data.capacity:
            self.trains_queue.pop(0)  # Only pop if we're going to process
            self.add_train_to_track(train_to_process)
            self.state = TerminalState.DISTRIBUTING
            train_to_process.state = TrainState.LOADING
        else:
            self.state = TerminalState.ACCUMULATING

    def step(self):
        if self.state == TerminalState.ACCUMULATING:
            self.data.stock += self.generate_normal_distribution()

            self.check_queue()
   