from pydantic import BaseModel, Field


class StationData(BaseModel):
    name: str
    loading_speed: int = Field(alias="loading_speed_train")
    unloading_speed: int | None = Field(alias="unloading_speed_train")
    stock: int
    stock_max: int | None = None
    total_functional_tracks: int = Field(alias="railways")
    production: dict
   