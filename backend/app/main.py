import asyncio
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.database import engine, Base
from app.api.routes import router
from app.services.simulator import run_simulator

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: create tables and launch the sensor simulator
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    simulator_task = asyncio.create_task(run_simulator())
    yield
    # Shutdown: cancel simulator
    simulator_task.cancel()
    try:
        await simulator_task
    except asyncio.CancelledError:
        pass


app = FastAPI(
    title="Sensor Monitor API",
    description="Real-time sensor monitoring system",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api")
