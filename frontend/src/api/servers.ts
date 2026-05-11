import client from "./client";
import type {
  ApiResponse,
  CreateServerPayload,
  PageData,
  Server,
  ServerFilters,
  UpdateServerPayload,
} from "@/types";

export const serversApi = {
  list: (params?: ServerFilters) =>
    client
      .get<ApiResponse<PageData<Server>>>("/servers", { params })
      .then((r) => r.data),

  get: (id: string) =>
    client.get<ApiResponse<Server>>(`/servers/${id}`).then((r) => r.data),

  create: (data: CreateServerPayload) =>
    client.post<ApiResponse<Server>>("/servers", data).then((r) => r.data),

  update: (id: string, data: UpdateServerPayload) =>
    client.put<ApiResponse<Server>>(`/servers/${id}`, data).then((r) => r.data),

  delete: (id: string) =>
    client.delete<ApiResponse<null>>(`/servers/${id}`).then((r) => r.data),
};
