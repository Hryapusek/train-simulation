from pydantic import BaseModel

class Terminal(BaseModel):
    name: str
    loading_speed_train: int
    unloading_speed_train: int | None = None
    stock: int
    stock_max: int | None = None
    railways: int
    production: dict
   