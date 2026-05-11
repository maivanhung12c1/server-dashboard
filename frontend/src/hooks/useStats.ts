import { useState, useEffect } from "react";
import { statsApi } from "@/api/stats";
import type { OverviewStats, TimeseriesStats } from "@/types";

export function useOverviewStats() {
  const [data, setData] = useState<OverviewStats | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    statsApi
      .overview()
      .then((res) => setData(res.data))
      .catch((err) =>
        setError(err instanceof Error ? err.message : "Failed to load stats"),
      )
      .finally(() => setLoading(false));
  }, []);

  return { data, loading, error };
}

export function useTimeseriesStats(
  range: "24h" | "7d" | "30d" | "custom",
  start?: string,
  end?: string,
) {
  const [data, setData] = useState<TimeseriesStats | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    setLoading(true);
    statsApi
      .timeseries({ range, start, end })
      .then((res) => setData(res.data))
      .catch((err) =>
        setError(
          err instanceof Error ? err.message : "Failed to load timeseries",
        ),
      )
      .finally(() => setLoading(false));
  }, [range, start, end]);

  return { data, loading, error };
}
