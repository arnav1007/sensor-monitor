# Sensor Monitor

Real-time temperature monitoring dashboard with anomaly detection.

## Architecture

```
├── backend/          FastAPI + SQLAlchemy (async)
│   ├── app/
│   │   ├── api/          REST endpoints
│   │   ├── core/         Config, database engine
│   │   ├── models/       SQLAlchemy ORM models
│   │   ├── schemas/      Pydantic response schemas
│   │   └── services/     Business logic + simulator
│   └── requirements.txt
├── frontend/         React + TypeScript (Vite)
│   └── src/
│       ├── api/          Axios API client
│       ├── components/   SensorCard, AlertsPanel, ReadingsTable, etc.
│       ├── hooks/        useSensorData (polling hook)
│       ├── types/        TypeScript interfaces
│       └── utils/        Shared constants, formatters, temp helpers
└── docker-compose.yml    PostgreSQL container
```

## Quick Start

**Prerequisites:** Docker, Python 3.11+, Node.js 18+

```bash
# 1. Start PostgreSQL
docker compose up -d

# 2. Start backend
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000

# 3. Start frontend (new terminal)
cd frontend
npm install
npm run dev
```

Open **http://localhost:5173** — the dashboard auto-refreshes every 30 seconds.

## API Endpoints

| Endpoint | Description |
|---|---|
| `GET /api/sensors` | List all sensors |
| `GET /api/sensors/{id}/readings` | Last 10 readings for a sensor |
| `GET /api/alerts` | All readings above 80°C |

## Design Decisions

- **Simulator runs as a FastAPI background task** — no extra process to manage. Each sensor has a realistic base temperature with Gaussian drift and a 10% spike probability to exercise alerts and anomaly detection.
- **Anomaly detection is computed at query time** — the 1-hour rolling average is calculated per sensor when readings are fetched, keeping the schema simple and the detection logic easy to tune.
- **CSS Modules for component styling** — scoped class names with no global collisions, each component owns its styles.
- **Single shared constants file** — thresholds (70°C warning, 80°C critical), polling interval, and color palette defined once.

## Approach

I structured the system around clear separation of concerns: the simulator generates realistic sensor data as a background task, FastAPI serves it through clean async endpoints, and React polls and renders the state with color-coded temperature cards. Anomaly detection flags any reading that exceeds 15% above its sensor's 1-hour rolling average, computed server-side at query time to keep the data model simple.
