export interface Sensor {
  id: number;
  name: string;
  location: string;
  created_at: string;
}

export interface Reading {
  id: number;
  sensor_id: number;
  temperature: number;
  timestamp: string;
  is_anomaly: boolean;
}

export interface Alert {
  id: number;
  sensor_id: number;
  sensor_name: string;
  temperature: number;
  timestamp: string;
  is_anomaly: boolean;
}
