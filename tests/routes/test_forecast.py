from datetime import date
import pytest
from fastapi.testclient import TestClient
from app.database.schemas import City, Forecast
from app.main import app
from app.database.database import get_db, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"  # Use a separate test DB
engine = create_engine(SQLALCHEMY_DATABASE_URL,
                       connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False,
                                   autoflush=False,
                                   bind=engine)


@pytest.fixture(scope="module")
def test_db():
    Base.metadata.create_all(bind=engine)
    yield TestingSessionLocal()
    Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def client(test_db):

    def override_get_db():
        try:
            yield test_db
        finally:
            test_db.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as client:
        yield client


class TestForecastCRUD:

    def test_create_forecast(self, client, test_db):
        city = City(name="London")
        test_db.add(city)
        test_db.commit()

        payload = {
            "forecast_date": "2024-10-27",
            "city_id": 1,
            "temperature": 20.5,
            "humidity": 50.0,
            "wind": 5.0,
        }

        response = client.post("/forecasts/", json=payload)
        assert response.status_code == 200
        assert response.json()["forecast_date"] == "2024-10-27"

    def test_create_forecast_city_does_not_exist(self, client, test_db):
        city = City(name="London")
        test_db.add(city)
        test_db.commit()

        payload = {
            "forecast_date": "2024-10-27",
            "city_id": 999,
            "temperature": 20.5,
            "humidity": 50.0,
            "wind": 5.0,
        }

        response = client.post("/forecasts/", json=payload)
        assert response.status_code == 400
        assert response.json()["detail"] == "Selected city does not exist"

    def test_create_forecast_already_exists(self, client, test_db):
        city = City(name="Paris")
        test_db.add(city)
        test_db.commit()

        payload = {
            "forecast_date": "2024-10-27",
            "city_id": 1,
            "temperature": 20.5,
            "humidity": 50.0,
            "wind": 5.0,
        }

        client.post("/forecasts/", json=payload)
        response = client.post("/forecasts/", json=payload)

        assert response.status_code == 400
        assert response.json(
        )["detail"] == "Forecast for this city on this date already exists."

    def test_read_forecast(self, client, test_db):
        forecast = Forecast(forecast_date=date(2024, 10, 26),
                            city_id=1,
                            temperature=22,
                            humidity=55.0,
                            wind=6.0)
        test_db.add(forecast)
        test_db.commit()

        response = client.get("/forecasts/1")
        assert response.status_code == 200
        assert response.json()["id"] == 1

    def test_update_forecast(self, client, test_db):
        city = City(name="Paris")
        forecast = Forecast(forecast_date=date(2024, 10, 26),
                            city_id=1,
                            temperature=22,
                            humidity=55.0,
                            wind=6.0)
        test_db.add(forecast)
        test_db.add(city)
        test_db.commit()

        payload = {
            "forecast_date": "2024-10-27",
            "city_id": 1,
            "temperature": 22.0,
            "humidity": 56.0,
            "wind": 6.0,
        }

        response = client.put("/forecasts/1", json=payload)

        assert response.status_code == 200
        assert response.json()["forecast_date"] == "2024-10-27"

    def test_update_forecast_does_not_exist(self, client):

        payload = {
            "forecast_date": "2024-10-27",
            "city_id": 1,
            "temperature": 22.0,
            "humidity": 56.0,
            "wind": 6.0,
        }

        response = client.put("/forecasts/23", json=payload)
        assert response.status_code == 404
        assert response.json()["detail"] == "Forecast not found"

    def test_update_forecast_city_does_not_exist(self, client, test_db):
        forecast = Forecast(forecast_date=date(2024, 10, 26),
                            city_id=1,
                            temperature=22,
                            humidity=55.0,
                            wind=6.0)
        test_db.add(forecast)
        test_db.commit()
        payload = {
            "forecast_date": "2024-10-27",
            "city_id": 10,
            "temperature": 22.0,
            "humidity": 56.0,
            "wind": 6.0,
        }

        response = client.put("/forecasts/1", json=payload)
        assert response.status_code == 404
        assert response.json()["detail"] == "Selected city does not exist"

    def test_delete_forecast(self, client, test_db):
        forecast = Forecast(forecast_date=date(2024, 10, 26),
                            city_id=1,
                            temperature=22,
                            humidity=55.0,
                            wind=6.0)
        test_db.add(forecast)
        test_db.commit()  # Commit the forecast

        response = client.delete("/forecasts/1")
        assert response.status_code == 200
        assert response.json()["detail"] == "Forecast deleted successfully"

        response = client.get("/forecasts/1")
        assert response.status_code == 404
