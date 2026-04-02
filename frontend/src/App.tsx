import { useSensorData } from "./hooks/useSensorData";
import Header from "./components/Header";
import SensorCard from "./components/SensorCard";
import AlertsPanel from "./components/AlertsPanel";
import "./App.css";

function App() {
  const { sensors, readings, alerts, loading, error, lastUpdated, refresh } =
    useSensorData();

  if (loading) {
    return (
      <div className="loading">
        <div className="spinner" />
        <p>Loading sensor data...</p>
      </div>
    );
  }

  return (
    <div className="app">
      <Header lastUpdated={lastUpdated} onRefresh={refresh} />

      {error && (
        <div className="error-banner">
          <p>Unable to connect to the server: {error}</p>
          <button onClick={refresh}>Retry</button>
        </div>
      )}

      <main>
        <section className="sensors-grid">
          {sensors.map((sensor) => (
            <SensorCard
              key={sensor.id}
              sensor={sensor}
              readings={readings[sensor.id] ?? []}
            />
          ))}
        </section>
        <AlertsPanel alerts={alerts} />
      </main>
    </div>
  );
}

export default App;
