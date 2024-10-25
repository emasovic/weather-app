from pydantic import BaseModel
from datetime import date


class City(BaseModel):
    id: int
    name: str


class ForecastPayload(BaseModel):
    city_id: int
    forecast_date: date
    temperature: float
    humidity: float
    wind: float


class ForecastResponseItem(BaseModel):
    id: int
    forecast_date: date
    city: City
    temperature: float
    humidity: float
    wind: float

    class Config:
        orm_mode = True
