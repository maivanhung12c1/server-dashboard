import {
  Bar,
  BarChart,
  Cell,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import type { NameCount } from "@/types";

const PALETTE = [
  "#3b82f6",
  "#10b981",
  "#f59e0b",
  "#8b5cf6",
  "#ec4899",
  "#06b6d4",
];

const TooltipContent = ({ active, payload, label }: any) => {
  if (!active || !payload?.length) return null;
  return (
    <div className="card px-3 py-2 text-xs shadow-xl">
      <p className="text-slate-400 mb-0.5">{label}</p>
      <p className="text-white font-semibold">{payload[0].value} servers</p>
    </div>
  );
};

interface Props {
  title: string;
  data: NameCount[];
  loading?: boolean;
}

export default function ChartCard({ title, data, loading }: Props) {
  return (
    <div className="card p-5">
      <h3 className="text-sm font-semibold text-slate-300 mb-4">{title}</h3>
      {loading ? (
        <div className="h-44 flex items-center justify-center">
          <div className="w-6 h-6 border-2 border-blue-500 border-t-transparent rounded-full animate-spin" />
        </div>
      ) : data.length === 0 ? (
        <div className="h-44 flex items-center justify-center text-slate-600 text-sm">
          No data available
        </div>
      ) : (
        <ResponsiveContainer width="100%" height={176}>
          <BarChart
            data={data}
            layout="vertical"
            margin={{ left: 8, right: 16 }}
          >
            <XAxis type="number" hide />
            <YAxis
              type="category"
              dataKey="name"
              tick={{ fontSize: 11, fill: "#94a3b8" }}
              width={80}
              tickLine={false}
              axisLine={false}
            />
            <Tooltip
              content={<TooltipContent />}
              cursor={{ fill: "rgba(255,255,255,0.04)" }}
            />
            <Bar dataKey="count" radius={[0, 4, 4, 0]}>
              {data.map((_, i) => (
                <Cell key={i} fill={PALETTE[i % PALETTE.length]} />
              ))}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      )}
    </div>
  );
}
