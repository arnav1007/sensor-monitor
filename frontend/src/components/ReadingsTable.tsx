import type { Reading } from "../types/sensor";
import { getTempColorSet, formatTemperature } from "../utils/temperature";
import { formatTime } from "../utils/format";
import { THRESHOLDS } from "../utils/constants";
import StatusBadge from "./StatusBadge";
import styles from "./ReadingsTable.module.css";

interface Props {
  readings: Reading[];
}

export default function ReadingsTable({ readings }: Props) {
  return (
    <div className={styles.wrapper}>
      <h3>Recent Readings</h3>
      {readings.length === 0 ? (
        <p className={styles.noData}>No readings yet</p>
      ) : (
        <table className={styles.table}>
          <thead>
            <tr>
              <th>Temperature</th>
              <th>Time</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            {readings.map((r) => (
              <tr key={r.id}>
                <td className={styles.tempCell} style={{ color: getTempColorSet(r.temperature).text }}>
                  {formatTemperature(r.temperature)}
                </td>
                <td>{formatTime(r.timestamp)}</td>
                <td>
                  {r.is_anomaly && <StatusBadge type="anomaly" />}
                  {r.temperature >= THRESHOLDS.CRITICAL && <StatusBadge type="alert" />}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}
