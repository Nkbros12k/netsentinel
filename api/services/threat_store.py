"""In-memory ring buffer for recent threat detections."""

import asyncio
import time
from collections import deque
from datetime import datetime


class ThreatStore:
    def __init__(self, maxlen: int = 1000):
        self._buffer: deque = deque(maxlen=maxlen)
        self._lock = asyncio.Lock()
        self._total = 0
        self._threats = 0
        self._attack_counts: dict[str, int] = {}
        self._start_time = time.time()
        self._ws_clients: set = set()

    async def add(self, record: dict):
        async with self._lock:
            self._total += 1
            if record["prediction"] != "Normal":
                self._threats += 1
                attack = record["attack_type"]
                self._attack_counts[attack] = self._attack_counts.get(attack, 0) + 1
                self._buffer.append(record)

        if record["prediction"] != "Normal":
            await self._broadcast(record)

    async def _broadcast(self, record: dict):
        dead = set()
        import json
        msg = json.dumps(record, default=str)
        for ws in self._ws_clients:
            try:
                await ws.send_text(msg)
            except Exception:
                dead.add(ws)
        self._ws_clients -= dead

    def register_ws(self, ws):
        self._ws_clients.add(ws)

    def unregister_ws(self, ws):
        self._ws_clients.discard(ws)

    def get_stats(self) -> dict:
        uptime = time.time() - self._start_time
        rate = (self._threats / uptime * 60) if uptime > 0 else 0
        return {
            "total_processed": self._total,
            "threats_detected": self._threats,
            "threat_rate": round(rate, 2),
            "attack_breakdown": dict(self._attack_counts),
            "uptime_seconds": round(uptime, 1),
        }

    def get_recent(self, n: int = 50) -> list:
        return list(self._buffer)[-n:]


store = ThreatStore()
