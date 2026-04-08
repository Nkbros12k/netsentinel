import { useEffect, useState } from "react";
import type { Stats } from "../types";

export function useStats(interval = 3000) {
  const [stats, setStats] = useState<Stats>({
    total_processed: 0,
    threats_detected: 0,
    threat_rate: 0,
    attack_breakdown: {},
    uptime_seconds: 0,
  });

  useEffect(() => {
    const apiBase = import.meta.env.VITE_API_URL || "";

    const fetchStats = async () => {
      try {
        const res = await fetch(`${apiBase}/stats`);
        if (res.ok) setStats(await res.json());
      } catch { /* retry next interval */ }
    };

    fetchStats();
    const id = setInterval(fetchStats, interval);
    return () => clearInterval(id);
  }, [interval]);

  return stats;
}
