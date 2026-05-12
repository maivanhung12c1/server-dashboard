import { Globe, X } from "lucide-react";
import { useEffect, useState } from "react";
import { mapApi } from "@/api/map";
import WorldMap from "@/components/map/WorldMap";
import type { MapCountryData } from "@/types";

export default function MapView() {
  const [data, setData] = useState<MapCountryData[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    setLoading(true);
    setError(null);
    mapApi
      .getData()
      .then((res) => setData(res.data))
      .catch((err) =>
        setError(err instanceof Error ? err.message : "Failed to load map data"),
      )
      .finally(() => setLoading(false));
  }, []);

  const totalServers = data.reduce((sum, d) => sum + d.count, 0);

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-xl font-bold text-white">Server Map</h1>
          <p className="text-sm text-slate-500 mt-0.5">
            Geographic distribution of servers
          </p>
        </div>
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

      {/* Stats row */}
      <div className="grid grid-cols-2 gap-4 sm:grid-cols-3 lg:w-1/2">
        <div className="card p-4 flex items-center gap-3">
          <div className="w-8 h-8 rounded-lg bg-blue-500/10 flex items-center justify-center">
            <Globe size={16} className="text-blue-400" />
          </div>
          <div>
            <p className="text-xs text-slate-500">Countries</p>
            <p className="text-lg font-bold text-white">
              {loading ? "—" : data.length}
            </p>
          </div>
        </div>
        <div className="card p-4 flex items-center gap-3">
          <div className="w-8 h-8 rounded-lg bg-emerald-500/10 flex items-center justify-center">
            <span className="text-emerald-400 text-xs font-bold">SRV</span>
          </div>
          <div>
            <p className="text-xs text-slate-500">Mapped Servers</p>
            <p className="text-lg font-bold text-white">
              {loading ? "—" : totalServers}
            </p>
          </div>
        </div>
      </div>

      {/* Map */}
      <WorldMap data={data} loading={loading} />

      {/* Country table */}
      {!loading && data.length > 0 && (
        <div className="card overflow-hidden">
          <div className="px-5 py-3 border-b border-slate-700/50">
            <h3 className="text-sm font-semibold text-slate-300">By Country</h3>
          </div>
          <div className="divide-y divide-slate-700/30">
            {[...data]
              .sort((a, b) => b.count - a.count)
              .map((item) => (
                <div
                  key={item.country}
                  className="flex items-center justify-between px-5 py-3 hover:bg-slate-800/30 transition-colors"
                >
                  <span className="text-sm text-slate-200">{item.country}</span>
                  <div className="flex items-center gap-3">
                    <div className="flex gap-1">
                      {item.servers.slice(0, 4).map((s) => (
                        <span
                          key={s.id}
                          className={`w-2 h-2 rounded-full ${s.status === "Online" ? "bg-emerald-400" : "bg-red-400"}`}
                          title={`${s.name} — ${s.status}`}
                        />
                      ))}
                      {item.servers.length > 4 && (
                        <span className="text-xs text-slate-600">
                          +{item.servers.length - 4}
                        </span>
                      )}
                    </div>
                    <span className="text-xs text-slate-400 w-16 text-right">
                      {item.count} server{item.count !== 1 ? "s" : ""}
                    </span>
                  </div>
                </div>
              ))}
          </div>
        </div>
      )}
    </div>
  );
}
