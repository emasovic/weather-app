from datetime import datetime
from sqlalchemy import Column, DateTime, Float, Date, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from enum import Enum
from .database import Base


class City(Base):
    __tablename__ = "city"
    id = Column(
        Integer,
        primary_key=True,
    )
    name = Column(String, nullable=False)

    forecasts = relationship("Forecast", back_populates="city")
    stations = relationship("Station", back_populates="city")


class Station(Base):
    __tablename__ = "stations"
    id = Column(
        Integer,
        primary_key=True,
    )
    code = Column(String, unique=True, nullable=False)
    city_id = Column(Integer, ForeignKey("city.id"), nullable=False)

    latitude = Column(Float)
    longitude = Column(Float)
    date_of_installation = Column(Date)

    city = relationship("City", back_populates="stations")
    sensors = relationship("Sensor", back_populates="station")


class Sensor(Base):
    __tablename__ = "sensors"
    id = Column(Integer, primary_key=True)
    station_code = Column(String, ForeignKey("stations.code"), nullable=False)

    station = relationship("Station", back_populates="sensors")
    measurements = relationship("Measurement", back_populates="sensor")


class Measurement(Base):
    __tablename__ = "measurements"
    id = Column(Integer, primary_key=True)
    sensor_id = Column(Integer, ForeignKey("sensors.id"), nullable=False)
    measurement_time = Column(DateTime, default=datetime.utcnow)
    category = Column(String, nullable=False)
    value = Column(Float, nullable=False)
    unit = Column(String, nullable=False)

    sensor = relationship("Sensor", back_populates="measurements")


class Forecast(Base):
    __tablename__ = "forecasts"
    id = Column(Integer, primary_key=True)
    forecast_date = Column(Date, nullable=False)
    city_id = Column(Integer, ForeignKey("city.id"), nullable=False)
    temperature = Column(Float, nullable=True)
    humidity = Column(Float, nullable=True)
    wind = Column(Float, nullable=True)

    city = relationship("City", back_populates="forecasts")
