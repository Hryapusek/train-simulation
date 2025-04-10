from pydantic import BaseModel
from enum import Enum
from core.train import Train 

class TerminalModel(BaseModel):

    name: str
    loading_speed_train: int
    unloading_speed_train: int | None = None
    stock: int
    stock_max: int | None = None
    railways: int
    production: dict
   
class TerminalState(Enum):
    # Загружаем в терминал
    TAKE_FUEL = 1
    # Выгружаем в поезд
    GIVEAWAY_FUEL = 2


class Terminal:

    def __init__(self, terminal: TerminalModel) -> None:
        self.name = terminal.name    
        self.stock = terminal.stock
        self.railways = terminal.railways    
        self.loading_speed_train = terminal.loading_speed_train    
        self.unloading_speed_train = terminal.unloading_speed_train

    def define_terminal_state(self, train: Train) -> TerminalState:
        if self.stock >= train.capacity and self.railways == 0:
            return TerminalState.TAKE_FUEL
        else:
            return TerminalState.GIVEAWAY_FUEL
