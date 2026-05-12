import { useState, useEffect } from "react";
import { activitiesApi } from "@/api/activity";
import type { Activity } from "@/types";

export function useActivities(limit = 10, refreshKey = 0) {
  const [data, setData] = useState<Activity[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    setLoading(true);
    setError(null);
    activitiesApi
      .list(limit)
      .then((res) => setData(res.data))
      .catch((err) =>
        setError(err instanceof Error ? err.message : "Failed to load activities"),
      )
      .finally(() => setLoading(false));
  }, [limit, refreshKey]);

  return { data, loading, error };
}
