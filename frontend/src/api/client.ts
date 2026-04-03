import axios from "axios";
import type { Sensor, Reading, Alert } from "../types/sensor";

const API_BASE_URL =
  import.meta.env.VITE_API_URL ?? "https://sensor-monitor-api.onrender.com/api";

const api = axios.create({ baseURL: API_BASE_URL });

export async function fetchSensors(): Promise<Sensor[]> {
  const { data } = await api.get<Sensor[]>("/sensors");
  return data;
}

export async function fetchReadings(sensorId: number): Promise<Reading[]> {
  const { data } = await api.get<Reading[]>(`/sensors/${sensorId}/readings`);
  return data;
}

export async function fetchAlerts(): Promise<Alert[]> {
  const { data } = await api.get<Alert[]>("/alerts");
  return data;
}
