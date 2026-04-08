import { useEffect, useRef, useState, useCallback } from "react";
import type { ThreatEvent } from "../types";

const MAX_EVENTS = 200;

export function useWebSocket(url: string) {
  const [events, setEvents] = useState<ThreatEvent[]>([]);
  const [connected, setConnected] = useState(false);
  const wsRef = useRef<WebSocket | null>(null);
  const retryRef = useRef(0);

  const connect = useCallback(() => {
    const ws = new WebSocket(url);
    wsRef.current = ws;

    ws.onopen = () => {
      setConnected(true);
      retryRef.current = 0;
    };

    ws.onmessage = (e) => {
      const event: ThreatEvent = JSON.parse(e.data);
      setEvents((prev) => [event, ...prev].slice(0, MAX_EVENTS));
    };

    ws.onclose = () => {
      setConnected(false);
      const delay = Math.min(1000 * 2 ** retryRef.current, 10000);
      retryRef.current++;
      setTimeout(connect, delay);
    };

    ws.onerror = () => ws.close();
  }, [url]);

  useEffect(() => {
    connect();
    return () => wsRef.current?.close();
  }, [connect]);

  return { events, connected };
}
