from pydantic import BaseModel, Field

class TrainData(BaseModel):
    name: str
    speed: int | None = None
    capacity: int
    route_name: str = Field(alias="road")
    volume: int
    target_station_name: str | None
    distance_travelled: int
    
