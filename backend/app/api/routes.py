from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.sensor import SensorOut, ReadingOut, AlertOut
from app.services import sensor_service

router = APIRouter()


@router.get("/sensors", response_model=list[SensorOut])
async def list_sensors(db: AsyncSession = Depends(get_db)):
    """List all sensors."""
    return await sensor_service.get_all_sensors(db)


@router.get("/sensors/{sensor_id}/readings", response_model=list[ReadingOut])
async def get_readings(sensor_id: int, db: AsyncSession = Depends(get_db)):
    """Get the last 10 readings for a sensor, with anomaly flags."""
    readings = await sensor_service.get_sensor_readings(db, sensor_id)
    if not readings:
        raise HTTPException(status_code=404, detail="Sensor not found or no readings yet")
    return readings


@router.get("/alerts", response_model=list[AlertOut])
async def get_alerts(db: AsyncSession = Depends(get_db)):
    """Get all readings above the alert threshold (80°C)."""
    return await sensor_service.get_alerts(db)
