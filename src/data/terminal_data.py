from pydantic import BaseModel, Field


class TerminalData(BaseModel):
    name: str
    loading_speed: int
    stock: int
    total_functional_tracks: int
    production_mean: float
    production_deviation: float
   