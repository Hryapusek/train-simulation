from __future__ import annotations
from data.train_data import TrainData
from datetime import datetime
from enum import Enum, auto

# TODO: comment me otherwise you will get error
# from simulation.simulation import Simulation
# from .station_simulator import StationSimulator

class StationType(Enum):
    TERMINAL = auto()
    TRANSFER_POINT = auto()

class TrainState(Enum):
    # Двигаемся
    MOVING = auto()
    # Загружаемся
    LOADING = auto()
    # Разгружаемся
    UNLOADING = auto()
    # Ожидаем
    IN_QUEUE = auto()


class Direction(Enum):
    TERMINAL_TO_TRANSFER_POINT = auto()
    TRANSFER_POINT_TO_TERMINAL = auto()


class TrainSimulator:
    def __init__(self, train_data: TrainData, simulation: "Simulation"):
        self.data = train_data
        self.parent_simulation = simulation

        self.route = self.parent_simulation.get_route_by_name(self.data.route_name)
        self.stations_dict = self.get_route_endpoints()

        self.direction = self.define_direction()
        self.state = self.define_initial_state()

        self.delayed_step = False

    
    def __repr__(self):
        return f"TrainSimulator(train_data={self.data.name}, direction={self.direction}, state={self.state})"
    
    def __str__(self):
        return f"TrainSimulator(train_data={self.data.name}, direction={self.direction}, state={self.state})"

    def get_route_endpoints(self): 
        station_a, station_type_a = self.parent_simulation.get_station_with_type(
            self.route.departure_station_name
        )
        station_b, station_type_b = self.parent_simulation.get_station_with_type(
            self.route.destination_station_name
        )
        return {
            station_type_a: station_a,
            station_type_b: station_b,
        }  # station_type is StationType

    def define_direction(self):
        target_station_name = self.data.target_station_name
        if self.route.destination_station_name == target_station_name:
            return Direction.TERMINAL_TO_TRANSFER_POINT
        elif self.route.departure_station_name == target_station_name:
            return Direction.TRANSFER_POINT_TO_TERMINAL
        assert False

    def toggle_direction(self):
        self.data.distance_travelled = 0

        if self.direction == Direction.TERMINAL_TO_TRANSFER_POINT:
            self.direction = Direction.TRANSFER_POINT_TO_TERMINAL
            return
        elif self.direction == Direction.TRANSFER_POINT_TO_TERMINAL:
            self.direction = Direction.TERMINAL_TO_TRANSFER_POINT
            return
        assert False

    def get_target_station_with_type(self):
        if self.direction == Direction.TERMINAL_TO_TRANSFER_POINT:
            return self.stations_dict[StationType.TRANSFER_POINT], StationType.TRANSFER_POINT
        elif self.direction == Direction.TRANSFER_POINT_TO_TERMINAL:
            return self.stations_dict[StationType.TERMINAL], StationType.TERMINAL

    def define_initial_state(self):
        # Cache frequently accessed attributes
        distance_travelled = self.data.distance_travelled
        route_distance = self.route.distance
        volume = self.data.volume
        capacity = self.data.capacity

        # Early exit for moving state (most common case)
        if distance_travelled != route_distance:
            return TrainState.MOVING

        # Get station info
        station: "StationSimulator"
        station, station_type = self.get_target_station_with_type()
        station_available_tracks = station.count_available_tracks()

        # Pre-compute load states
        train_is_full = volume == capacity
        train_is_empty = volume == 0

        # Check track availability
        if station_available_tracks == 0:
            station.add_train_to_queue(self)
            return TrainState.IN_QUEUE

        # Handle terminal station case
        if station_type == StationType.TERMINAL:
            if train_is_full:
                station.on_train_left(self)
                self.toggle_direction()
                return TrainState.MOVING
            if station.data.stock >= capacity:
                station.add_train_to_track(self)
                station.redefine_state()
                return TrainState.LOADING
            else:
                station.add_train_to_queue(self)
                return TrainState.IN_QUEUE
        
        # Handle transfer station case
        if station_type == StationType.TRANSFER_POINT:
            if train_is_empty:
                station.on_train_left(self)
                self.toggle_direction()
                return TrainState.MOVING
            station.add_train_to_track(self)
            station.redefine_state()
            return TrainState.UNLOADING

        raise AssertionError("This should be unreachable")
            
    def redefine_state(self):
        state = self.state  # Faster local access
        volume = self.data.volume
        train_is_full = volume == self.data.capacity
        train_is_empty = volume == 0

        if state == TrainState.IN_QUEUE:
            # Train is waiting for availible track; station will handle state change
            return state # no changes

        station: "StationSimulator"
        station, station_type = self.get_target_station_with_type()
        station_available_tracks = station.count_available_tracks()

        if state == TrainState.MOVING:
            return self._redefine_moving_state(station, station_type, station_available_tracks)

        if state == TrainState.LOADING:
            return self._redefine_loading_state(station, train_is_full)

        if state == TrainState.UNLOADING:
            return self._redefine_unloading_state(station, train_is_empty)

        raise AssertionError("Unknown train state")


    def _redefine_moving_state(self, station: "StationSimulator", station_type, station_available_tracks):
        if self.data.distance_travelled != self.route.distance:
            return TrainState.MOVING  # Still traveling

        if station_available_tracks == 0:
            station.add_train_to_queue(self)
            return TrainState.IN_QUEUE

        if station.trains_queue:    #even if there are available tracks, there is another train in queue waiting for when enough oil is accumulated
            station.add_train_to_queue(self)
            return TrainState.IN_QUEUE      #FIFO
        
        if station_type == StationType.TERMINAL:
            if station.data.stock >= self.data.capacity:
                station.add_train_to_track(self)
                station.redefine_state()
                return TrainState.LOADING
            station.add_train_to_queue(self)
            return TrainState.IN_QUEUE

        if station_type == StationType.TRANSFER_POINT:
            station.add_train_to_track(self)
            station.redefine_state()
            return TrainState.UNLOADING

        raise AssertionError("Unhandled station type")


    def _redefine_loading_state(self, station: "StationSimulator", train_is_full):
        if train_is_full:
            station.on_train_left(self)
            self.toggle_direction()
            return TrainState.MOVING
        return TrainState.LOADING


    def _redefine_unloading_state(self, station: "StationSimulator", train_is_empty):
        if train_is_empty:
            station.on_train_left(self)
            self.toggle_direction()
            return TrainState.MOVING
        return TrainState.UNLOADING
    
    
    def step_moving(self):
        # Здесь мы просто двигаем поезд вперед на self.speed
        left_to_go = self.route.distance - self.data.distance_travelled
        if left_to_go <= self.data.speed:
            self.data.distance_travelled += left_to_go
        else:
            self.data.distance_travelled += self.data.speed
        self.state = self.redefine_state()

    def step_loading(self):
        # # мы находимся на терминале и загружаемся - берем из терминала топливо
        terminal = self.stations_dict[StationType.TERMINAL]
        self.data.volume += terminal.give_fuel(self)
        self.state = self.redefine_state()
        pass

    def step_unloading(self):
        # мы находимся на п.п. и разгружаемся - отдаем топливо в п.п.
        transfer_point = self.stations_dict[StationType.TRANSFER_POINT]
        self.data.volume -= transfer_point.take_fuel(self)
        self.state = self.redefine_state()
        pass

    def step_waiting(self):
        # час ниче не делаем и никаких изменений в систему не вносим
        self.state = self.redefine_state()
        pass

    def simulate_step(self):
        train_state = self.state

        if train_state == TrainState.IN_QUEUE:
            self.step_waiting()

        elif train_state == TrainState.MOVING:
            self.step_moving()

        elif train_state == TrainState.LOADING:
            self.step_loading()

        elif train_state == TrainState.UNLOADING:
            self.step_unloading()

