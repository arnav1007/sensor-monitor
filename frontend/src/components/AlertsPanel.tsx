import type { Alert } from "../types/sensor";
import { formatTime } from "../utils/format";
import { formatTemperature } from "../utils/temperature";
import StatusBadge from "./StatusBadge";
import styles from "./AlertsPanel.module.css";

interface Props {
  alerts: Alert[];
}

export default function AlertsPanel({ alerts }: Props) {
  return (
    <div className={styles.panel}>
      <h2 className={styles.title}>
        Alerts <span className={styles.count}>{alerts.length}</span>
      </h2>
      {alerts.length === 0 ? (
        <p className={styles.noData}>No alerts — all readings below 80°C</p>
      ) : (
        <div className={styles.list}>
          {alerts.map((a) => (
            <div key={a.id} className={styles.item}>
              <div className={styles.info}>
                <strong>{a.sensor_name}</strong>
                <span className={styles.temp}>{formatTemperature(a.temperature)}</span>
                {a.is_anomaly && <StatusBadge type="anomaly" />}
              </div>
              <span className={styles.time}>{formatTime(a.timestamp)}</span>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
