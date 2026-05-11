import { type LucideIcon } from "lucide-react";
import clsx from "clsx";

interface Props {
  label: string;
  value: number | string;
  icon: LucideIcon;
  color?: "blue" | "green" | "red" | "yellow" | "purple";
  subtitle?: string;
  loading?: boolean;
}

const colorMap = {
  blue: "text-blue-400 bg-blue-500/10 border-blue-500/20",
  green: "text-emerald-400 bg-emerald-500/10 border-emerald-500/20",
  red: "text-red-400 bg-red-500/10 border-red-500/20",
  yellow: "text-yellow-400 bg-yellow-500/10 border-yellow-500/20",
  purple: "text-purple-400 bg-purple-500/10 border-purple-500/20",
};

export default function StatCard({
  label,
  value,
  icon: Icon,
  color = "blue",
  subtitle,
  loading,
}: Props) {
  if (loading) {
    return (
      <div className="card p-5">
        <div className="animate-pulse space-y-2">
          <div className="h-3 bg-slate-700 rounded w-24" />
          <div className="h-8 bg-slate-700 rounded w-16" />
        </div>
      </div>
    );
  }

  return (
    <div className="card p-5">
      <div className="flex items-start justify-between">
        <div>
          <p className="text-xs font-medium uppercase tracking-wider text-slate-400 mb-2">
            {label}
          </p>
          <p className="text-3xl font-bold text-white">{value}</p>
          {subtitle && (
            <p className="text-xs text-slate-500 mt-1">{subtitle}</p>
          )}
        </div>
        <div
          className={clsx(
            "w-10 h-10 rounded-lg flex items-center justify-center border",
            colorMap[color],
          )}
        >
          <Icon size={18} />
        </div>
      </div>
    </div>
  );
}
