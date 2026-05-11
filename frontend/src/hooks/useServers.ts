import { useState, useCallback } from "react";
import { serversApi } from "@/api/servers";
import type {
  Server,
  PageData,
  ServerFilters,
  CreateServerPayload,
  UpdateServerPayload,
} from "@/types";

export function useServers() {
  const [data, setData] = useState<PageData<Server> | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchServers = useCallback(async (filters?: ServerFilters) => {
    setLoading(true);
    setError(null);
    try {
      const res = await serversApi.list(filters);
      setData(res.data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to fetch servers");
    } finally {
      setLoading(false);
    }
  }, []);

  const createServer = useCallback(
    async (payload: CreateServerPayload): Promise<Server> => {
      const res = await serversApi.create(payload);
      return res.data;
    },
    [],
  );

  const updateServer = useCallback(
    async (id: string, payload: UpdateServerPayload): Promise<Server> => {
      const res = await serversApi.update(id, payload);
      return res.data;
    },
    [],
  );

  const deleteServer = useCallback(async (id: string): Promise<void> => {
    await serversApi.delete(id);
  }, []);

  return {
    data,
    loading,
    error,
    fetchServers,
    createServer,
    updateServer,
    deleteServer,
  };
}
