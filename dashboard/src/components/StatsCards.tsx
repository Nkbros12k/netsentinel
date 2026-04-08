import { Activity, AlertTriangle, Gauge, Clock } from "lucide-react";
import type { Stats } from "../types";

function Card({
  icon: Icon,
  label,
  value,
  color,
}: {
  icon: React.ElementType;
  label: string;
  value: string;
  color: string;
}) {
  return (
    <div className="bg-slate-800/50 border border-slate-700/50 rounded-xl p-4 flex items-center gap-4">
      <div className={`w-10 h-10 rounded-lg flex items-center justify-center ${color}`}>
        <Icon size={18} />
      </div>
      <div>
        <p className="text-xs text-slate-400">{label}</p>
        <p className="text-xl font-bold text-white">{value}</p>
      </div>
    </div>
  );
}

export function StatsCards({ stats }: { stats: Stats }) {
  const formatUptime = (s: number) => {
    if (s < 60) return `${Math.floor(s)}s`;
    if (s < 3600) return `${Math.floor(s / 60)}m`;
    return `${Math.floor(s / 3600)}h ${Math.floor((s % 3600) / 60)}m`;
  };

  return (
    <div className="grid grid-cols-2 lg:grid-cols-4 gap-3">
      <Card
        icon={Activity}
        label="Total Processed"
        value={stats.total_processed.toLocaleString()}
        color="bg-cyan-500/20 text-cyan-400"
      />
      <Card
        icon={AlertTriangle}
        label="Threats Detected"
        value={stats.threats_detected.toLocaleString()}
        color="bg-red-500/20 text-red-400"
      />
      <Card
        icon={Gauge}
        label="Threats / min"
        value={stats.threat_rate.toFixed(1)}
        color="bg-amber-500/20 text-amber-400"
      />
      <Card
        icon={Clock}
        label="Uptime"
        value={formatUptime(stats.uptime_seconds)}
        color="bg-emerald-500/20 text-emerald-400"
      />
    </div>
  );
}
