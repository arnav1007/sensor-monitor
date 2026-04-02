import styles from "./StatusBadge.module.css";

interface Props {
  type: "anomaly" | "alert" | "anomalyBanner";
  label?: string;
}

const DEFAULT_LABELS: Record<Props["type"], string> = {
  anomaly: "ANOMALY",
  alert: "ALERT",
  anomalyBanner: "ANOMALY DETECTED",
};

export default function StatusBadge({ type, label }: Props) {
  return (
    <span className={styles[type]}>{label ?? DEFAULT_LABELS[type]}</span>
  );
}
