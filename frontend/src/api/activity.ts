import client from "./client";
import type { Activity, ApiResponse } from "@/types";

export const activitiesApi = {
  list: (limit = 20) =>
    client
      .get<ApiResponse<Activity[]>>("/activities", { params: { limit } })
      .then((r) => r.data),
};
