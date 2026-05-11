import { Edit2, Trash2 } from "lucide-react";
import type { Server } from "@/types";

const COLUMNS = [
  "Name",
  "IP Address",
  "Country",
  "OS / Version",
  "Platform",
  "Arch",
  "Status",
  "Updated",
  "",
];

function SkeletonRow() {
  return (
    <tr>
      {COLUMNS.map((_, i) => (
        <td key={i} className="px-4 py-3">
          <div className="h-4 bg-slate-700/60 rounded animate-pulse" />
        </td>
      ))}
    </tr>
  );
}

interface Props {
  servers: Server[];
  loading: boolean;
  onEdit: (server: Server) => void;
  onDelete: (id: string, name: string) => void;
}

export default function ServerTable({
  servers,
  loading,
  onEdit,
  onDelete,
}: Props) {
  return (
    <div className="overflow-x-auto rounded-xl border border-slate-700/50">
      <table className="w-full text-sm">
        <thead>
          <tr className="border-b border-slate-700/50 bg-dark-900/50">
            {COLUMNS.map((h) => (
              <th key={h} className="table-header">
                {h}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {loading ? (
            Array.from({ length: 6 }).map((_, i) => <SkeletonRow key={i} />)
          ) : servers.length === 0 ? (
            <tr>
              <td
                colSpan={COLUMNS.length}
                className="text-center py-16 text-slate-600 text-sm"
              >
                No servers found
              </td>
            </tr>
          ) : (
            servers.map((srv) => (
              <tr
                key={srv.id}
                className="border-b border-slate-700/30 hover:bg-slate-800/30 transition-colors"
              >
                <td className="table-cell font-medium text-white">
                  {srv.name}
                </td>
                <td className="table-cell font-mono text-xs text-slate-400">
                  {srv.ip_address}
                </td>
                <td className="table-cell">{srv.country}</td>
                <td className="table-cell">
                  <span className="text-slate-200">{srv.os}</span>
                  <span className="text-slate-500 text-xs ml-1">
                    {srv.os_version}
                  </span>
                </td>
                <td className="table-cell">{srv.platform}</td>
                <td className="table-cell">
                  <span className="text-xs bg-slate-700/60 text-slate-300 px-2 py-0.5 rounded">
                    {srv.arch}
                  </span>
                </td>
                <td className="table-cell">
                  {srv.status === "Online" ? (
                    <span className="badge-online">
                      <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse" />
                      Online
                    </span>
                  ) : (
                    <span className="badge-offline">
                      <span className="w-1.5 h-1.5 rounded-full bg-red-400" />
                      Offline
                    </span>
                  )}
                </td>
                <td className="table-cell text-xs text-slate-500 whitespace-nowrap">
                  {srv.updated_at}
                </td>
                <td className="table-cell">
                  <div className="flex items-center gap-1">
                    <button
                      onClick={() => onEdit(srv)}
                      className="p-1.5 text-slate-500 hover:text-blue-400 hover:bg-blue-500/10 rounded transition-colors"
                      title="Edit"
                    >
                      <Edit2 size={13} />
                    </button>
                    <button
                      onClick={() => onDelete(srv.id, srv.name)}
                      className="p-1.5 text-slate-500 hover:text-red-400 hover:bg-red-500/10 rounded transition-colors"
                      title="Delete"
                    >
                      <Trash2 size={13} />
                    </button>
                  </div>
                </td>
              </tr>
            ))
          )}
        </tbody>
      </table>
    </div>
  );
}
