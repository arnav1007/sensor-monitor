import asyncio
import random
import logging
from datetime import datetime, timezone

from sqlalchemy import select

from app.core.config import settings
from app.core.database import async_session
from app.models.sensor import Sensor, Reading

logger = logging.getLogger(__name__)

# Each sensor has a base temperature with small normal drift.
# ~10% chance of a spike to test alerts and anomaly detection.
DEFAULT_SENSORS = [
    {"name": "Sensor-A", "location": "Server Room 1", "base_temp": 45.0},
    {"name": "Sensor-B", "location": "Server Room 2", "base_temp": 55.0},
    {"name": "Sensor-C", "location": "Warehouse", "base_temp": 38.0},
]

# sensor_id -> base_temp mapping, populated after seeding
_base_temps: dict[int, float] = {}


async def seed_sensors():
    """Create the 3 default sensors if they don't exist."""
    async with async_session() as db:
        result = await db.execute(select(Sensor))
        existing = result.scalars().all()

        if len(existing) >= 3:
            for sensor, defaults in zip(existing, DEFAULT_SENSORS):
                _base_temps[sensor.id] = defaults["base_temp"]
            logger.info("Sensors already seeded.")
            return

        for s in DEFAULT_SENSORS:
            db.add(Sensor(name=s["name"], location=s["location"]))
        await db.commit()

        result = await db.execute(select(Sensor))
        for sensor, defaults in zip(result.scalars().all(), DEFAULT_SENSORS):
            _base_temps[sensor.id] = defaults["base_temp"]
        logger.info("Seeded 3 default sensors.")


def _generate_temperature(sensor_id: int) -> float:
    """Generate a realistic temperature reading.

    Normal readings fluctuate ±3°C around the base.
    ~10% of the time, a spike of +20-40°C occurs.
    """
    base = _base_temps.get(sensor_id, 50.0)
    if random.random() < 0.10:
        # Spike: push into alert/anomaly territory
        temperature = base + random.uniform(20.0, 40.0)
    else:
        # Normal drift
        temperature = base + random.gauss(0, 3.0)
    return round(max(20.0, min(95.0, temperature)), 2)


async def generate_reading():
    """Generate one temperature reading per sensor."""
    async with async_session() as db:
        result = await db.execute(select(Sensor))
        sensors = result.scalars().all()

        for sensor in sensors:
            temperature = _generate_temperature(sensor.id)
            reading = Reading(
                sensor_id=sensor.id,
                temperature=temperature,
                timestamp=datetime.now(timezone.utc),
            )
            db.add(reading)
            logger.info(f"{sensor.name}: {temperature}°C")

        await db.commit()


async def run_simulator():
    """Background loop: seed sensors, then emit readings every SIMULATOR_INTERVAL seconds."""
    await seed_sensors()
    logger.info(f"Simulator started — interval: {settings.SIMULATOR_INTERVAL}s")

    while True:
        try:
            await generate_reading()
        except Exception as e:
            logger.error(f"Simulator error: {e}")
        await asyncio.sleep(settings.SIMULATOR_INTERVAL)
