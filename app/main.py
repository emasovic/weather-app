from fastapi import FastAPI

from app.database.database import Base, engine
from app.database.initial_insert import insert_initial_cities

from .routers import forecasts

app = FastAPI()

app.include_router(forecasts.router, prefix='/forecasts', tags=['Forecasts'])

Base.metadata.create_all(bind=engine)
insert_initial_cities()
