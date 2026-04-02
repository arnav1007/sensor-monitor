from datetime import datetime

from pydantic import BaseModel


class SensorOut(BaseModel):
    id: int
    name: str
    location: str
    created_at: datetime

    model_config = {"from_attributes": True}


class ReadingOut(BaseModel):
    id: int
    sensor_id: int
    temperature: float
    timestamp: datetime
    is_anomaly: bool = False

    model_config = {"from_attributes": True}


class AlertOut(BaseModel):
    id: int
    sensor_id: int
    sensor_name: str
    temperature: float
    timestamp: datetime
    is_anomaly: bool = False

    model_config = {"from_attributes": True}
