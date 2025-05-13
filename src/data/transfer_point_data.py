from pydantic import BaseModel, Field


class TransferPointData(BaseModel):
    name: str
    loading_speed: int
    unloading_speed: int | None
    stock: int
    stock_max: int | None = None
    total_functional_tracks: int
    departure_train_capacity: int
    departure_train_volume: int
   