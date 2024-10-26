from pydantic import BaseModel
from datetime import date


class ForecastPayload(BaseModel):
    city_id: int
    forecast_date: date
    temperature: float
    humidity: float
    wind: float
