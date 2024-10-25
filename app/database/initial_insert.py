from app.database.schemas import City
from app.database.database import SessionLocal


def insert_initial_cities():
    session = SessionLocal()
    city_count = session.query(City).count()

    if city_count == 0:
        cities = ["London", "Paris", "New York"]
        city_objects = [City(name=name) for name in cities]

        session.add_all(city_objects)
        session.commit()

    session.close()
