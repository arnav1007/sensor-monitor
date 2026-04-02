import { THRESHOLDS, COLORS } from "./constants";

type ColorSet = (typeof COLORS)[keyof typeof COLORS];

export function getTempColorSet(temp: number): ColorSet {
  if (temp >= THRESHOLDS.CRITICAL) return COLORS.red;
  if (temp >= THRESHOLDS.WARNING) return COLORS.yellow;
  return COLORS.green;
}

export function formatTemperature(temp: number): string {
  return `${temp.toFixed(1)}°C`;
}
