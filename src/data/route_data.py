from pydantic import BaseModel, Field


class RouteData(BaseModel):
    name: str
    departure_station_name: str = Field(alias="point_from")
    destination_station_name: str | None = Field(alias="point_to")
    distance: int | None

   
