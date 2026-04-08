import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip } from "recharts";

const COLORS: Record<string, string> = {
  DoS: "#ef4444",
  Probe: "#f59e0b",
  R2L: "#a855f7",
  U2R: "#f43f5e",
};

export function AttackTypesPie({ breakdown }: { breakdown: Record<string, number> }) {
  const data = Object.entries(breakdown)
    .filter(([k]) => k !== "Normal")
    .map(([name, value]) => ({ name, value }));

  if (data.length === 0) {
    return (
      <div className="bg-slate-800/50 border border-slate-700/50 rounded-xl p-4 flex flex-col items-center justify-center h-full">
        <h3 className="text-sm font-medium text-slate-400 mb-3">Attack Types</h3>
        <p className="text-slate-500 text-sm">Waiting for data...</p>
      </div>
    );
  }

  return (
    <div className="bg-slate-800/50 border border-slate-700/50 rounded-xl p-4">
      <h3 className="text-sm font-medium text-slate-400 mb-3">Attack Types</h3>
      <ResponsiveContainer width="100%" height={160}>
        <PieChart>
          <Pie data={data} dataKey="value" nameKey="name" cx="50%" cy="50%" innerRadius={40} outerRadius={65} paddingAngle={3}>
            {data.map((entry) => (
              <Cell key={entry.name} fill={COLORS[entry.name] || "#64748b"} />
            ))}
          </Pie>
          <Tooltip
            contentStyle={{ background: "#1e293b", border: "1px solid #334155", borderRadius: "8px", fontSize: 12 }}
          />
        </PieChart>
      </ResponsiveContainer>
      <div className="flex flex-wrap justify-center gap-3 mt-2">
        {data.map((d) => (
          <div key={d.name} className="flex items-center gap-1.5 text-xs text-slate-400">
            <div className="w-2 h-2 rounded-full" style={{ background: COLORS[d.name] || "#64748b" }} />
            {d.name} ({d.value})
          </div>
        ))}
      </div>
    </div>
  );
}
