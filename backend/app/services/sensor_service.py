from datetime import datetime, timedelta, timezone

from sqlalchemy import select, desc, text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.core.config import settings
from app.models.sensor import Sensor, Reading


async def get_all_sensors(db: AsyncSession) -> list[Sensor]:
    result = await db.execute(select(Sensor).order_by(Sensor.id))
    return list(result.scalars().all())


async def get_sensor_readings(db: AsyncSession, sensor_id: int, limit: int = 10) -> list[dict]:
    """Get last N readings for a sensor, with anomaly flag."""
    one_hour_ago = datetime.now(timezone.utc) - timedelta(hours=1)

    # Get the 1-hour rolling average for this sensor
    avg_result = await db.execute(
        select(Reading.temperature)
        .where(Reading.sensor_id == sensor_id, Reading.timestamp >= one_hour_ago)
    )
    recent_temps = [row[0] for row in avg_result.all()]
    rolling_avg = sum(recent_temps) / len(recent_temps) if recent_temps else None

    # Get last N readings
    result = await db.execute(
        select(Reading)
        .where(Reading.sensor_id == sensor_id)
        .order_by(desc(Reading.timestamp))
        .limit(limit)
    )
    readings = list(result.scalars().all())

    # Flag anomalies: reading > rolling_avg * (1 + ANOMALY_PERCENT/100)
    enriched = []
    for r in readings:
        is_anomaly = False
        if rolling_avg and rolling_avg > 0:
            threshold = rolling_avg * (1 + settings.ANOMALY_PERCENT / 100)
            is_anomaly = r.temperature > threshold
        enriched.append({
            "id": r.id,
            "sensor_id": r.sensor_id,
            "temperature": r.temperature,
            "timestamp": r.timestamp,
            "is_anomaly": is_anomaly,
        })

    return enriched


async def get_alerts(db: AsyncSession) -> list[dict]:
    """Get all readings above the alert threshold, with anomaly flag."""
    one_hour_ago = datetime.now(timezone.utc) - timedelta(hours=1)

    result = await db.execute(
        select(Reading, Sensor.name)
        .join(Sensor)
        .where(Reading.temperature > settings.ALERT_THRESHOLD)
        .order_by(desc(Reading.timestamp))
        .limit(50)
    )
    rows = result.all()

    # Compute rolling averages per sensor for anomaly detection
    sensor_ids = {row[0].sensor_id for row in rows}
    rolling_avgs = {}
    for sid in sensor_ids:
        avg_result = await db.execute(
            select(Reading.temperature)
            .where(Reading.sensor_id == sid, Reading.timestamp >= one_hour_ago)
        )
        temps = [r[0] for r in avg_result.all()]
        rolling_avgs[sid] = sum(temps) / len(temps) if temps else None

    alerts = []
    for reading, sensor_name in rows:
        avg = rolling_avgs.get(reading.sensor_id)
        is_anomaly = False
        if avg and avg > 0:
            is_anomaly = reading.temperature > avg * (1 + settings.ANOMALY_PERCENT / 100)
        alerts.append({
            "id": reading.id,
            "sensor_id": reading.sensor_id,
            "sensor_name": sensor_name,
            "temperature": reading.temperature,
            "timestamp": reading.timestamp,
            "is_anomaly": is_anomaly,
        })

    return alerts
