from pydantic import BaseModel


class OtherData(BaseModel):
    datetime_start: str
    datetime_end: str
    
