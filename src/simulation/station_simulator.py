from abc import ABC, abstractmethod

import numpy as np
from datetime import datetime
from enum import Enum, auto

from data.terminal_data import TerminalData
from data.transfer_point_data import TransferPointData

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
    def __init__(self, total_functional_tracks: int, simulation: int):
        self.parent_simulation = simulation
        self.tracks_status: list[TrainSimulator | None] = [None] * total_functional_tracks
        self.trains_queue: list[TrainSimulator] = []

    @abstractmethod
    def simulate_step(self):
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
    def __init__(self, data: TransferPointData, simulation):
        self.data = data
        self.data.total_functional_tracks -= 1
        StationSimulator.__init__(self, data.total_functional_tracks, simulation)
        # One is always reserved for ghost train
        self.state = TransferPointState.IDLE
        self.last_loaded: int = None

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
        train_to_process.delayed_step = True

    def simulate_step(self):
        if self.state == TransferPointState.ACCUMULATING:
            if self.data.stock >= self.data.departure_train_capacity:
                self.state = TransferPointState.DISTRIBUTING
                return

        if self.state == TransferPointState.DISTRIBUTING:
            left_to_load = self.data.departure_train_capacity - self.data.departure_train_volume

            if left_to_load >= self.data.loading_speed: 
                amount_to_load = self.data.loading_speed
            else:
                amount_to_load = left_to_load

            self.last_loaded = amount_to_load
            self.data.stock -= amount_to_load
            self.data.departure_train_volume += amount_to_load

            if self.data.departure_train_volume == self.data.departure_train_capacity:
                self.state = TransferPointState.ACCUMULATING
                self.data.departure_train_volume = 0 #reset the ghost train


class TerminalSimulator(StationSimulator):
    def __init__(self, data: TerminalData, simulation):
        StationSimulator.__init__(self, data.total_functional_tracks, simulation)
        self.data = data
        self.state = TerminalState.ACCUMULATING
        self.last_production_result = None # FOR LOGS
        
    def generate_normal_distribution(self):
        self.last_production_result = np.random.normal(self.data.production_mean, self.data.production_deviation)
        return self.last_production_result
    
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

    def simulate_step(self):
        if self.state == TerminalState.ACCUMULATING:
            self.data.stock += self.generate_normal_distribution()

            self.check_queue()
   

      # if self.count_trains_on_tracks() > 0:
        #     self.state = TransferPointState.ACCUMULATING    
        # else:
        #     self.state = TransferPointState.IDLE
        
        
        
    # if self.state == TerminalState.ACCUMULATING:
        #     return      #accumulating will turn itself off when it finishes in the step() -> check_queue()
        
        # if self.count_trains_on_tracks() > 0:
        #     self.state = TerminalState.DISTRIBUTING