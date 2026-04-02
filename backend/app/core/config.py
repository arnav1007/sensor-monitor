from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/sensor_monitor"
    SIMULATOR_INTERVAL: int = 30  # seconds between readings
    ALERT_THRESHOLD: float = 80.0  # °C
    ANOMALY_PERCENT: float = 15.0  # % above rolling average

    class Config:
        env_file = ".env"


settings = Settings()
