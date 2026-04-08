import { Shield } from "lucide-react";

export function Header({ connected }: { connected: boolean }) {
  return (
    <header className="flex items-center justify-between px-6 py-4 border-b border-slate-800">
      <div className="flex items-center gap-3">
        <div className="w-9 h-9 rounded-lg bg-cyan-500/20 flex items-center justify-center">
          <Shield size={20} className="text-cyan-400" />
        </div>
        <div>
          <h1 className="text-lg font-semibold text-white leading-tight">NetSentinel</h1>
          <p className="text-xs text-slate-500">Real-Time Threat Detection</p>
        </div>
      </div>
      <div className="flex items-center gap-2">
        <div
          className={`w-2 h-2 rounded-full ${connected ? "bg-emerald-400 animate-pulse" : "bg-red-500"}`}
        />
        <span className={`text-xs ${connected ? "text-emerald-400" : "text-red-400"}`}>
          {connected ? "Live" : "Disconnected"}
        </span>
      </div>
    </header>
  );
}
