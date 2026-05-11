import { Cpu, RefreshCw, Server, TrendingUp, Wifi } from "lucide-react";
import { useState } from "react";
import ActivityLog from "@/components/dashboard/ActivityLog";
import ChartCard from "@/components/dashboard/ChartCard";
import StatCard from "@/components/dashboard/StatCard";
import TimeseriesChart from "@/components/dashboard/TimeseriesChart";
import { useActivities } from "@/hooks/useActivities";
import { useOverviewStats, useTimeseriesStats } from "@/hooks/useStats";

type Range = "24h" | "7d" | "30d";

const RANGES: { label: string; value: Range }[] = [
  { label: "24h", value: "24h" },
  { label: "7 days", value: "7d" },
  { label: "30 days", value: "30d" },
];

export default function Dashboard() {
  const [range, setRange] = useState<Range>("7d");

  const { data: overview, loading: overviewLoading } = useOverviewStats();
  const { data: timeseries, loading: timeseriesLoading } =
    useTimeseriesStats(range);
  const { data: activities, loading: activityLoading } = useActivities(15);

  const onlineCount =
    overview?.by_status.find((s) => s.name === "Online")?.count ?? 0;
  const offlineCount =
    overview?.by_status.find((s) => s.name === "Offline")?.count ?? 0;

  function refresh() {
    window.location.reload();
  }

  return (
    <div className="space-y-6">
      {/* Page header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-xl font-bold text-white">Dashboard</h1>
          <p className="text-sm text-slate-500 mt-0.5">
            Server infrastructure overview
          </p>
        </div>
        <button onClick={refresh} className="btn-ghost">
          <RefreshCw size={14} />
          Refresh
        </button>
      </div>

      {/* Stat cards */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        <StatCard
          label="Total Servers"
          value={overview?.total_servers ?? "—"}
          icon={Server}
          color="blue"
          loading={overviewLoading}
        />
        <StatCard
          label="Online"
          value={onlineCount}
          icon={Wifi}
          color="green"
          loading={overviewLoading}
        />
        <StatCard
          label="Offline"
          value={offlineCount}
          icon={Cpu}
          color="red"
          loading={overviewLoading}
        />
        <StatCard
          label={`New (${range})`}
          value={timeseries?.new_in_range ?? "—"}
          icon={TrendingUp}
          color="yellow"
          loading={timeseriesLoading}
          subtitle={`of ${overview?.total_servers ?? 0} total`}
        />
      </div>

      {/* Top metric charts */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <ChartCard
          title="Top Operating Systems"
          data={overview?.by_os ?? []}
          loading={overviewLoading}
        />
        <ChartCard
          title="Top Platforms"
          data={overview?.by_platform ?? []}
          loading={overviewLoading}
        />
        <ChartCard
          title="Top Architectures"
          data={overview?.by_arch ?? []}
          loading={overviewLoading}
        />
      </div>

      {/* Timeseries + Activity */}
      <div className="grid grid-cols-1 xl:grid-cols-3 gap-4">
        {/* Timeseries chart */}
        <div className="xl:col-span-2 card p-5">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h3 className="text-sm font-semibold text-slate-300">
                Server Creation
              </h3>
              <p className="text-xs text-slate-500 mt-0.5">
                {timeseries?.new_in_range ?? 0} new in period
              </p>
            </div>
            <div className="flex gap-1">
              {RANGES.map((r) => (
                <button
                  key={r.value}
                  onClick={() => setRange(r.value)}
                  className={`px-2.5 py-1 text-xs rounded-lg transition-colors ${
                    range === r.value
                      ? "bg-blue-600 text-white"
                      : "text-slate-400 hover:text-white hover:bg-slate-800"
                  }`}
                >
                  {r.label}
                </button>
              ))}
            </div>
          </div>
          {timeseriesLoading ? (
            <div className="h-56 flex items-center justify-center">
              <div className="w-6 h-6 border-2 border-blue-500 border-t-transparent rounded-full animate-spin" />
            </div>
          ) : (
            <TimeseriesChart data={timeseries?.timeseries ?? []} />
          )}
        </div>

        {/* Activity log */}
        <ActivityLog activities={activities} loading={activityLoading} />
      </div>
    </div>
  );
}
