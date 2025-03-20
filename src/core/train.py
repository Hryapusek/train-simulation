from pydantic import BaseModel

class Train(BaseModel):
    name: str
    speed: int | None = None
    capacity: int
    road: str
    volume: int
    position: dict

if __name__ == "__main__": #
    train1 = Train(name="trainRP1", speed=40, capacity=4000, road="Raduzhney-Polyarny", volume=4000, position={"destination": "Polyarny", "traveled_dist": 1250})
    train2 = Train(name="trainRP2", speed=40, capacity=4000, road="Raduzhney-Polyarny", volume=0, position={"destination": "Polyarny", "traveled_dist": 2500})
