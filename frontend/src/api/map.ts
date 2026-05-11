import client from "./client";
import type { ApiResponse, MapCountryData } from "@/types";

export const mapApi = {
  getData: () =>
    client.get<ApiResponse<MapCountryData[]>>("/map").then((r) => r.data),
};
