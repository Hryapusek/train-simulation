from pydantic import BaseModel

class Train(BaseModel):
    name: str
    speed: int | None = None
    capacity: int
    road: str
    volume: int
    position: dict
