from datetime import datetime
from pydantic import BaseModel, Field


class OtherData(BaseModel):
    datetime_start: datetime
    datetime_end: datetime
