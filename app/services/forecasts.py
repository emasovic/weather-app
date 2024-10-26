from sqlalchemy.orm import Session
from ..database.schemas import Forecast, City
from ..models.forecasts import ForecastPayload
from sqlalchemy.orm import joinedload
from uuid import UUID


class ForecastService:

    def __init__(self, db: Session):
        self.db = db

    def create_forecast(self, forecast_data: ForecastPayload) -> Forecast:
        existing_city = (self.db.query(City).filter(
            City.id == forecast_data.city_id).first())

        if not existing_city:
            raise Exception("Selected city does not exist")

        existing_forecast = self.db.query(Forecast).filter(
            Forecast.city_id == forecast_data.city_id,
            Forecast.forecast_date == forecast_data.forecast_date).first()

        if existing_forecast:
            raise Exception(
                "Forecast for this city on this date already exists.")

        new_forecast = Forecast(**forecast_data.dict())
        self.db.add(new_forecast)
        self.db.commit()
        self.db.refresh(new_forecast)
        return new_forecast

    def read_forecasts(self, skip: int = 0, limit: int = 10) -> list[Forecast]:
        return self.db.query(Forecast).options(joinedload(
            Forecast.city)).offset(skip).limit(limit).all()

    def read_forecast(self, forecast_id: int) -> Forecast:
        forecast = self.db.query(Forecast).options(joinedload(
            Forecast.city)).filter(Forecast.id == forecast_id).first()
        if forecast is None:
            raise Exception("Forecast not found")
        return forecast

    def update_forecast(self, forecast_id: int,
                        forecast_data: ForecastPayload) -> Forecast:
        db_forecast = self.db.query(Forecast).filter(
            Forecast.id == forecast_id).first()

        if db_forecast is None:
            raise Exception("Forecast not found")

        existing_city = (self.db.query(City).filter(
            City.id == forecast_data.city_id).first())

        if not existing_city:
            raise Exception("Selected city does not exist")

        db_forecast.forecast_date = forecast_data.forecast_date
        db_forecast.temperature = forecast_data.temperature
        db_forecast.humidity = forecast_data.humidity
        db_forecast.wind = forecast_data.wind
        db_forecast.city_id = forecast_data.city_id
        self.db.commit()
        self.db.refresh(db_forecast)
        return db_forecast

    def delete_forecast(self, forecast_id: int):
        db_forecast = self.db.query(Forecast).filter(
            Forecast.id == forecast_id).first()

        if db_forecast is None:
            raise Exception("Forecast not found")

        self.db.delete(db_forecast)
        self.db.commit()
