import client from "./client";
import type { ApiResponse, OverviewStats, TimeseriesStats } from "@/types";

export const statsApi = {
  overview: () =>
    client
      .get<ApiResponse<OverviewStats>>("/stats/overview")
      .then((r) => r.data),

  timeseries: (params: {
    range: "24h" | "7d" | "30d" | "custom";
    start?: string;
    end?: string;
  }) =>
    client
      .get<ApiResponse<TimeseriesStats>>("/stats/timeseries", { params })
      .then((r) => r.data),
};
