import { useState, useEffect, useCallback } from "react";
import type { Sensor, Reading, Alert } from "../types/sensor";
import { fetchSensors, fetchReadings, fetchAlerts } from "../api/client";
import { POLL_INTERVAL_MS } from "../utils/constants";

export function useSensorData() {
  const [sensors, setSensors] = useState<Sensor[]>([]);
  const [readings, setReadings] = useState<Record<number, Reading[]>>({});
  const [alerts, setAlerts] = useState<Alert[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [lastUpdated, setLastUpdated] = useState<Date | null>(null);

  const loadData = useCallback(async () => {
    try {
      setError(null);
      const sensorList = await fetchSensors();
      setSensors(sensorList);

      const readingsMap: Record<number, Reading[]> = {};
      await Promise.all(
        sensorList.map(async (sensor) => {
          try {
            readingsMap[sensor.id] = await fetchReadings(sensor.id);
          } catch {
            readingsMap[sensor.id] = [];
          }
        })
      );
      setReadings(readingsMap);

      const alertList = await fetchAlerts();
      setAlerts(alertList);

      setLastUpdated(new Date());
    } catch (err) {
      const message = err instanceof Error ? err.message : "Failed to fetch sensor data";
      setError(message);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    loadData();
    const interval = setInterval(loadData, POLL_INTERVAL_MS);
    return () => clearInterval(interval);
  }, [loadData]);

  return { sensors, readings, alerts, loading, error, lastUpdated, refresh: loadData };
}
