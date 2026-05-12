import { ChevronLeft, ChevronRight, Plus, Search, X } from "lucide-react";
import { useCallback, useEffect, useState } from "react";
import { serversApi } from "@/api/servers";
import ServerForm from "@/components/servers/ServerForm";
import ServerTable from "@/components/servers/ServerTable";
import type { CreateServerPayload, Server } from "@/types";

export default function Servers() {
  const [servers, setServers] = useState<Server[]>([]);
  const [total, setTotal] = useState(0);
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [editServer, setEditServer] = useState<Server | null>(null);

  const [search, setSearch] = useState("");
  const [statusFilter, setStatusFilter] = useState("");
  const [error, setError] = useState<string | null>(null);

  const size = 15;

  const fetchServers = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await serversApi.list({
        page,
        size,
        name: search || undefined,
        status: statusFilter || undefined,
      });
      setServers(res.data.items);
      setTotal(res.data.total);
      setTotalPages(res.data.total_pages);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load servers");
    } finally {
      setLoading(false);
    }
  }, [page, search, statusFilter]);

  useEffect(() => {
    fetchServers();
  }, [fetchServers]);

  const handleCreate = async (data: CreateServerPayload) => {
    await serversApi.create(data);
    fetchServers();
  };

  const handleUpdate = async (data: CreateServerPayload) => {
    if (editServer) {
      await serversApi.update(editServer.id, data);
      fetchServers();
    }
  };

  const handleDelete = async (id: string, name: string) => {
    if (!confirm(`Delete server "${name}"?`)) return;
    try {
      await serversApi.delete(id);
      fetchServers();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to delete server");
    }
  };

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    setPage(1);
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-xl font-bold text-white">Servers</h1>
          <p className="text-sm text-slate-500 mt-0.5">{total} total servers</p>
        </div>
        <button
          onClick={() => {
            setEditServer(null);
            setShowForm(true);
          }}
          className="btn-primary"
        >
          <Plus size={15} />
          Add Server
        </button>
      </div>

      {error && (
        <div className="px-4 py-3 bg-red-500/10 border border-red-500/20 rounded-lg flex items-center justify-between">
          <p className="text-sm text-red-400">{error}</p>
          <button
            onClick={() => setError(null)}
            className="text-red-400 hover:text-red-300 ml-4 flex-shrink-0"
          >
            <X size={14} />
          </button>
        </div>
      )}

      {/* Filters */}
      <div className="card p-4">
        <form onSubmit={handleSearch} className="flex items-center gap-3">
          <div className="relative flex-1 max-w-sm">
            <Search
              size={14}
              className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-500"
            />
            <input
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              placeholder="Search by name..."
              className="input pl-9"
            />
            {search && (
              <button
                type="button"
                onClick={() => {
                  setSearch("");
                  setPage(1);
                }}
                className="absolute right-3 top-1/2 -translate-y-1/2 text-slate-500 hover:text-white"
              >
                <X size={13} />
              </button>
            )}
          </div>
          <select
            value={statusFilter}
            onChange={(e) => {
              setStatusFilter(e.target.value);
              setPage(1);
            }}
            className="select w-36"
          >
            <option value="">All Status</option>
            <option value="Online">Online</option>
            <option value="Offline">Offline</option>
          </select>
          <button type="submit" className="btn-primary">
            Search
          </button>
        </form>
      </div>

      {/* Table */}
      <div className="card overflow-hidden">
        <ServerTable
          servers={servers}
          loading={loading}
          onEdit={(srv) => {
            setEditServer(srv);
            setShowForm(true);
          }}
          onDelete={handleDelete}
        />

        {totalPages > 1 && (
          <div className="flex items-center justify-between px-4 py-3 border-t border-slate-800">
            <p className="text-xs text-slate-500">
              Page {page} of {totalPages}
            </p>
            <div className="flex items-center gap-1">
              <button
                disabled={page <= 1}
                onClick={() => setPage((p) => p - 1)}
                className="p-1.5 text-slate-500 hover:text-white hover:bg-slate-800 rounded transition-colors disabled:opacity-30"
              >
                <ChevronLeft size={15} />
              </button>
              <button
                disabled={page >= totalPages}
                onClick={() => setPage((p) => p + 1)}
                className="p-1.5 text-slate-500 hover:text-white hover:bg-slate-800 rounded transition-colors disabled:opacity-30"
              >
                <ChevronRight size={15} />
              </button>
            </div>
          </div>
        )}
      </div>

      {showForm && (
        <ServerForm
          server={editServer}
          onClose={() => {
            setShowForm(false);
            setEditServer(null);
          }}
          onSubmit={editServer ? handleUpdate : handleCreate}
        />
      )}
    </div>
  );
}
