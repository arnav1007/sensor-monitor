import styles from "./Header.module.css";

interface Props {
  lastUpdated: Date | null;
  onRefresh: () => void;
}

export default function Header({ lastUpdated, onRefresh }: Props) {
  return (
    <header className={styles.header}>
      <div>
        <h1 className={styles.title}>Sensor Monitor</h1>
        <p className={styles.subtitle}>Real-time temperature monitoring dashboard</p>
      </div>
      <div className={styles.actions}>
        {lastUpdated && (
          <span className={styles.lastUpdated}>
            Updated: {lastUpdated.toLocaleTimeString()}
          </span>
        )}
        <button className={styles.refreshBtn} onClick={onRefresh}>
          Refresh
        </button>
      </div>
    </header>
  );
}
