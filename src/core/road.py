from pydantic import BaseModel

class Road(BaseModel):
    name: str
    point_from: str
    pointy_to: str | None = None
    distance: int | None = None
   
