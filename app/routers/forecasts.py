from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from ..database.database import get_db
from ..models.forecasts import ForecastPayload
from ..services.forecasts import ForecastService

router = APIRouter()


@router.post("/")
def create_forecast(forecast: ForecastPayload, db: Session = Depends(get_db)):
    service = ForecastService(db)
    try:
        return service.create_forecast(forecast)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/")
def read_forecasts(skip: int = 0,
                   limit: int = 10,
                   db: Session = Depends(get_db)):
    service = ForecastService(db)
    return service.read_forecasts(skip, limit)


@router.get("/{forecast_id}")
def read_forecast(forecast_id: int, db: Session = Depends(get_db)):
    service = ForecastService(db)
    try:
        return service.read_forecast(forecast_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put("/{forecast_id}")
def update_forecast(forecast_id: int,
                    forecast: ForecastPayload,
                    db: Session = Depends(get_db)):
    service = ForecastService(db)
    try:
        return service.update_forecast(forecast_id, forecast)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{forecast_id}", response_model=dict)
def delete_forecast(forecast_id: int, db: Session = Depends(get_db)):
    service = ForecastService(db)
    try:
        service.delete_forecast(forecast_id)
        return {"detail": "Forecast deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
