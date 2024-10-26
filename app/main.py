from fastapi import Depends, FastAPI, WebSocket
from pytest import Session

from app.models.sensors import SensorPayload
from app.services.sensors import SensorService

from .database.database import Base, engine, get_db
from .database.initial_insert import insert_initial_cities
from fastapi import FastAPI, WebSocket
from .routers import forecasts

app = FastAPI()

app.include_router(forecasts.router, prefix='/forecasts', tags=['Forecasts'])

Base.metadata.create_all(bind=engine)


@app.websocket("/ws/iot")
async def websocket_endpoint(websocket: WebSocket,
                             db: Session = Depends(get_db)):
    await websocket.accept()

    try:
        while True:
            data = await websocket.receive_json()
            sensor_payload = SensorPayload(**data)
            sensor_service = SensorService(db)
            sensor_service.create_measurements(sensor_payload)

            await websocket.send_text("Data received and stored successfully.")
    except Exception as e:
        await websocket.send_text(f"Error: {str(e)}")
        await websocket.close()


@app.on_event("startup")
async def startup_event():
    await insert_initial_cities()
