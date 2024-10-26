from typing import List
from pydantic import BaseModel
from datetime import datetime


class SensorInfo(BaseModel):
    category: str
    measurement: float
    unit: str


class SensorPayload(BaseModel):
    identifier: str
    sensor: str
    date: datetime
    city: str
    info: List[SensorInfo]
