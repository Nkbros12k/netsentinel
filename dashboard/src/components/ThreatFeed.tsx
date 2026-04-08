import type { ThreatEvent } from "../types";

const LEVEL_COLORS: Record<string, string> = {
  critical: "bg-red-500/20 text-red-400 border-red-500/30",
  high: "bg-orange-500/20 text-orange-400 border-orange-500/30",
  medium: "bg-amber-500/20 text-amber-400 border-amber-500/30",
  low: "bg-blue-500/20 text-blue-400 border-blue-500/30",
};

const TYPE_COLORS: Record<string, string> = {
  DoS: "bg-red-500",
  Probe: "bg-amber-500",
  R2L: "bg-purple-500",
  U2R: "bg-rose-500",
};

export function ThreatFeed({ events }: { events: ThreatEvent[] }) {
  const formatTime = (ts: string) => {
    const d = new Date(ts);
    return d.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit", second: "2-digit" });
  };

  return (
    <div className="bg-slate-800/50 border border-slate-700/50 rounded-xl p-4">
      <div className="flex items-center justify-between mb-3">
        <h3 className="text-sm font-medium text-slate-400">Live Threat Feed</h3>
        <span className="text-xs text-slate-500">{events.length} events</span>
      </div>
      <div className="space-y-1.5 max-h-[360px] overflow-y-auto pr-1">
        {events.length === 0 ? (
          <p className="text-slate-500 text-sm text-center py-8">Waiting for threats...</p>
        ) : (
          events.slice(0, 50).map((e, i) => (
            <div
              key={`${e.timestamp}-${i}`}
              className={`flex items-center gap-3 px-3 py-2 rounded-lg border ${LEVEL_COLORS[e.threat_level] || "bg-slate-700/30 text-slate-400 border-slate-600/30"}`}
              style={{ animation: i === 0 ? "fadeIn 0.3s ease" : undefined }}
            >
              <span className="text-xs text-slate-500 font-mono w-16 shrink-0">
                {formatTime(e.timestamp)}
              </span>
              <span className={`text-xs px-2 py-0.5 rounded font-medium text-white ${TYPE_COLORS[e.attack_type] || "bg-slate-600"}`}>
                {e.attack_type}
              </span>
              <div className="flex-1 h-1.5 bg-slate-700 rounded-full overflow-hidden">
                <div
                  className="h-full rounded-full transition-all"
                  style={{
                    width: `${e.confidence * 100}%`,
                    background: e.confidence > 0.9 ? "#ef4444" : e.confidence > 0.7 ? "#f59e0b" : "#22d3ee",
                  }}
                />
              </div>
              <span className="text-xs text-slate-500 font-mono w-12 text-right">
                {(e.confidence * 100).toFixed(0)}%
              </span>
            </div>
          ))
        )}
      </div>
      <style>{`@keyframes fadeIn { from { opacity: 0; transform: translateY(-4px); } to { opacity: 1; transform: translateY(0); } }`}</style>
    </div>
  );
}
