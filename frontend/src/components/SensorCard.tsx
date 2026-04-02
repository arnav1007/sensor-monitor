import type { Sensor, Reading } from "../types/sensor";
import { getTempColorSet, formatTemperature } from "../utils/temperature";
import { COLORS } from "../utils/constants";
import StatusBadge from "./StatusBadge";
import ReadingsTable from "./ReadingsTable";
import styles from "./SensorCard.module.css";

interface Props {
  sensor: Sensor;
  readings: Reading[];
}

export default function SensorCard({ sensor, readings }: Props) {
  const latest = readings[0];
  const currentTemp = latest?.temperature ?? null;
  const colors = currentTemp !== null ? getTempColorSet(currentTemp) : COLORS.neutral;

  return (
    <div className={styles.card} style={{ borderColor: colors.border }}>
      <div className={styles.header}>
        <div>
          <h2 className={styles.name}>{sensor.name}</h2>
          <p className={styles.location}>{sensor.location}</p>
        </div>
        {currentTemp !== null && (
          <div
            className={styles.tempDisplay}
            style={{ backgroundColor: colors.bg, color: colors.text }}
          >
            {formatTemperature(currentTemp)}
          </div>
        )}
      </div>

      {latest?.is_anomaly && <StatusBadge type="anomalyBanner" />}

      <ReadingsTable readings={readings} />
    </div>
  );
}
