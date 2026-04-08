import { useMemo } from "react";
import { AreaChart, Area, XAxis, YAxis, Tooltip, ResponsiveContainer } from "recharts";
import type { ThreatEvent } from "../types";

export function ThreatChart({ events }: { events: ThreatEvent[] }) {
  const data = useMemo(() => {
    const buckets = new Map<string, { dos: number; probe: number; r2l: number; u2r: number }>();

    for (const e of events) {
      const t = new Date(e.timestamp);
      const key = `${t.getHours().toString().padStart(2, "0")}:${t.getMinutes().toString().padStart(2, "0")}:${(Math.floor(t.getSeconds() / 10) * 10).toString().padStart(2, "0")}`;

      if (!buckets.has(key)) buckets.set(key, { dos: 0, probe: 0, r2l: 0, u2r: 0 });
      const b = buckets.get(key)!;
      const type = e.attack_type.toLowerCase();
      if (type === "dos") b.dos++;
      else if (type === "probe") b.probe++;
      else if (type === "r2l") b.r2l++;
      else if (type === "u2r") b.u2r++;
    }

    return Array.from(buckets.entries())
      .map(([time, counts]) => ({ time, ...counts }))
      .slice(-30);
  }, [events]);

  return (
    <div className="bg-slate-800/50 border border-slate-700/50 rounded-xl p-4">
      <h3 className="text-sm font-medium text-slate-400 mb-3">Threat Timeline</h3>
      <ResponsiveContainer width="100%" height={200}>
        <AreaChart data={data}>
          <defs>
            <linearGradient id="dosGrad" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stopColor="#ef4444" stopOpacity={0.4} />
              <stop offset="100%" stopColor="#ef4444" stopOpacity={0} />
            </linearGradient>
            <linearGradient id="probeGrad" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stopColor="#f59e0b" stopOpacity={0.4} />
              <stop offset="100%" stopColor="#f59e0b" stopOpacity={0} />
            </linearGradient>
          </defs>
          <XAxis dataKey="time" tick={{ fill: "#64748b", fontSize: 10 }} axisLine={false} tickLine={false} />
          <YAxis tick={{ fill: "#64748b", fontSize: 10 }} axisLine={false} tickLine={false} width={30} />
          <Tooltip
            contentStyle={{ background: "#1e293b", border: "1px solid #334155", borderRadius: "8px", fontSize: 12 }}
            labelStyle={{ color: "#94a3b8" }}
          />
          <Area type="monotone" dataKey="dos" name="DoS" stroke="#ef4444" fill="url(#dosGrad)" strokeWidth={2} />
          <Area type="monotone" dataKey="probe" name="Probe" stroke="#f59e0b" fill="url(#probeGrad)" strokeWidth={2} />
          <Area type="monotone" dataKey="r2l" name="R2L" stroke="#a855f7" fill="none" strokeWidth={1.5} />
          <Area type="monotone" dataKey="u2r" name="U2R" stroke="#f43f5e" fill="none" strokeWidth={1.5} />
        </AreaChart>
      </ResponsiveContainer>
    </div>
  );
}
