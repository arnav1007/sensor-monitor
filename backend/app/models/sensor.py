from datetime import datetime

from sqlalchemy import String, Float, DateTime, ForeignKey, Index, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Sensor(Base):
    __tablename__ = "sensors"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    location: Mapped[str] = mapped_column(String(200), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    readings: Mapped[list["Reading"]] = relationship(back_populates="sensor", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<Sensor id={self.id} name={self.name}>"


class Reading(Base):
    __tablename__ = "readings"
    __table_args__ = (
        Index("ix_readings_sensor_timestamp", "sensor_id", "timestamp"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    sensor_id: Mapped[int] = mapped_column(ForeignKey("sensors.id"), nullable=False)
    temperature: Mapped[float] = mapped_column(Float, nullable=False)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    sensor: Mapped["Sensor"] = relationship(back_populates="readings")

    def __repr__(self) -> str:
        return f"<Reading sensor={self.sensor_id} temp={self.temperature}°C>"
