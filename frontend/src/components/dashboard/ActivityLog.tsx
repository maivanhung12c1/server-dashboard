import { CheckCircle, Edit3, PlusCircle, Trash2 } from "lucide-react";
import type { Activity } from "@/types";

interface Props {
  activities: Activity[];
  loading: boolean;
}

const actionConfig = {
  created: {
    icon: PlusCircle,
    color: "text-emerald-400",
    bg: "bg-emerald-500/10",
    label: "created",
  },
  updated: {
    icon: CheckCircle,
    color: "text-blue-400",
    bg: "bg-blue-500/10",
    label: "updated",
  },
  renamed: {
    icon: Edit3,
    color: "text-yellow-400",
    bg: "bg-yellow-500/10",
    label: "renamed",
  },
  deleted: {
    icon: Trash2,
    color: "text-red-400",
    bg: "bg-red-500/10",
    label: "deleted",
  },
} as const;

export default function ActivityLog({ activities, loading }: Props) {
  return (
    <div className="card p-5">
      <h3 className="text-sm font-semibold text-slate-300 mb-4">
        Recent Activity
      </h3>
      {loading ? (
        <div className="space-y-3">
          {Array.from({ length: 6 }).map((_, i) => (
            <div
              key={i}
              className="h-12 bg-slate-800/50 rounded-lg animate-pulse"
            />
          ))}
        </div>
      ) : activities.length === 0 ? (
        <div className="text-center py-10 text-slate-600 text-sm">
          No recent activity
        </div>
      ) : (
        <div className="space-y-1.5 max-h-[28rem] overflow-y-auto pr-1">
          {activities.map((act) => {
            const cfg = actionConfig[act.action] ?? actionConfig.updated;
            const Icon = cfg.icon;
            return (
              <div
                key={act.id}
                className="flex items-start gap-3 p-2.5 rounded-lg hover:bg-slate-800/40 transition-colors"
              >
                <div
                  className={`w-6 h-6 rounded-full flex items-center justify-center flex-shrink-0 mt-0.5 ${cfg.bg}`}
                >
                  <Icon size={12} className={cfg.color} />
                </div>
                <div className="min-w-0 flex-1">
                  <p className="text-xs text-slate-200 leading-snug">
                    {act.detail}
                  </p>
                  <p className="text-xs text-slate-600 mt-0.5">
                    {act.timestamp}
                  </p>
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}
