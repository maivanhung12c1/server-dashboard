import { useState, useEffect } from "react";
import { activitiesApi } from "@/api/activity";
import type { Activity } from "@/types";

export function useActivities(limit = 10) {
  const [data, setData] = useState<Activity[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    activitiesApi
      .list(limit)
      .then((res) => setData(res.data))
      .catch(console.error)
      .finally(() => setLoading(false));
  }, [limit]);

  return { data, loading };
}
