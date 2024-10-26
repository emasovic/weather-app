from datetime import datetime
from app.database.schemas import City, Sensor, Station
from app.database.database import SessionLocal


async def insert_initial_cities():
    session = SessionLocal()

    if session.query(City).count() == 0:
        city_data = {"name": "London"}
        city = City(**city_data)
        session.add(city)
        session.commit()

        if session.query(Station).count() == 0:
            station_data = {
                "code": "LON-001",
                "city_id": city.id,
                "latitude": 51.5074,
                "longitude": -0.1278,
                "date_of_installation": datetime(2020, 1, 1)
            }
            station = Station(**station_data)
            session.add(station)
            session.commit()

            if session.query(Sensor).count() == 0:
                sensor_data = {
                    "station_code": station.code,
                }
                sensor = Sensor(**sensor_data)
                session.add(sensor)
                session.commit()
                print("Initial data created: City, Station, and Sensor.")
            else:
                print("Sensor table already has data.")
        else:
            print("Station table already has data.")
    else:
        print("City table already has data.")

    session.close()
