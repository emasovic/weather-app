from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.database.schemas import Measurement, Sensor, Station
from app.models.sensors import SensorPayload


class SensorService:

    def __init__(self, db: Session):
        self.db = db

    def create_measurements(self, sensor: SensorPayload) -> None:
        station = self.db.query(Station).filter_by(
            code=sensor.identifier).first()

        if not station:
            raise HTTPException(status_code=404, detail="Station not found")

        if not sensor.info or len(sensor.info) == 0:
            raise HTTPException(status_code=400,
                                detail="Sensor info not provided")

        for measurement_info in sensor.info:
            new_measurement = Measurement(sensor_id=sensor.sensor,
                                          measurement_time=sensor.date,
                                          category=measurement_info.category,
                                          value=measurement_info.measurement,
                                          unit=measurement_info.unit)
            self.db.add(new_measurement)

        self.db.commit()

        return None
