export const THRESHOLDS = {
  WARNING: 70,
  CRITICAL: 80,
} as const;

export const POLL_INTERVAL_MS = 30_000;

export const COLORS = {
  green: { text: "#16a34a", bg: "#f0fdf4", border: "#22c55e" },
  yellow: { text: "#ca8a04", bg: "#fefce8", border: "#eab308" },
  red: { text: "#dc2626", bg: "#fef2f2", border: "#ef4444" },
  neutral: { text: "#6b7280", bg: "#f9fafb", border: "#e5e7eb" },
} as const;
