import { useEffect, useRef, useState, useMemo } from "react";
import Globe from "react-globe.gl";
import type { ThreatEvent, ArcData } from "../types";

const CITY_COORDS: [number, number, string][] = [
  [40.7128, -74.006, "New York"],
  [51.5074, -0.1278, "London"],
  [35.6762, 139.6503, "Tokyo"],
  [55.7558, 37.6173, "Moscow"],
  [-33.8688, 151.2093, "Sydney"],
  [39.9042, 116.4074, "Beijing"],
  [48.8566, 2.3522, "Paris"],
  [37.5665, 126.978, "Seoul"],
  [1.3521, 103.8198, "Singapore"],
  [19.076, 72.8777, "Mumbai"],
  [-23.5505, -46.6333, "Sao Paulo"],
  [30.0444, 31.2357, "Cairo"],
  [52.52, 13.405, "Berlin"],
  [34.0522, -118.2437, "Los Angeles"],
  [43.6532, -79.3832, "Toronto"],
  [59.3293, 18.0686, "Stockholm"],
  [25.2048, 55.2708, "Dubai"],
  [-1.2921, 36.8219, "Nairobi"],
  [41.0082, 28.9784, "Istanbul"],
  [22.3193, 114.1694, "Hong Kong"],
];

const TARGET: [number, number] = [30.2672, -97.7431]; // Austin, TX

const ARC_COLORS: Record<string, string> = {
  DoS: "#ef4444",
  Probe: "#f59e0b",
  R2L: "#a855f7",
  U2R: "#f43f5e",
};

export function ThreatGlobe({ events }: { events: ThreatEvent[] }) {
  const globeRef = useRef<any>(null);
  const [arcs, setArcs] = useState<ArcData[]>([]);

  useEffect(() => {
    if (globeRef.current) {
      globeRef.current.pointOfView({ lat: 30, lng: -40, altitude: 2.2 }, 0);
      globeRef.current.controls().autoRotate = true;
      globeRef.current.controls().autoRotateSpeed = 0.5;
      globeRef.current.controls().enableZoom = true;
    }
  }, []);

  useEffect(() => {
    if (events.length === 0) return;
    const latest = events[0];
    const source = CITY_COORDS[Math.floor(Math.random() * CITY_COORDS.length)];
    const newArc: ArcData = {
      startLat: source[0],
      startLng: source[1],
      endLat: TARGET[0],
      endLng: TARGET[1],
      color: ARC_COLORS[latest.attack_type] || "#64748b",
      attack_type: latest.attack_type,
    };
    setArcs((prev) => [newArc, ...prev].slice(0, 30));
  }, [events.length]);

  const globeImageUrl = useMemo(
    () => "//unpkg.com/three-globe/example/img/earth-night.jpg",
    []
  );

  return (
    <div className="bg-slate-800/50 border border-slate-700/50 rounded-xl p-4 overflow-hidden">
      <h3 className="text-sm font-medium text-slate-400 mb-2">Global Threat Map</h3>
      <div className="flex justify-center" style={{ height: 350 }}>
        <Globe
          ref={globeRef}
          width={450}
          height={350}
          globeImageUrl={globeImageUrl}
          backgroundColor="rgba(0,0,0,0)"
          atmosphereColor="#22d3ee"
          atmosphereAltitude={0.15}
          arcsData={arcs}
          arcStartLat="startLat"
          arcStartLng="startLng"
          arcEndLat="endLat"
          arcEndLng="endLng"
          arcColor="color"
          arcDashLength={0.5}
          arcDashGap={0.2}
          arcDashAnimateTime={1500}
          arcStroke={0.5}
          arcsTransitionDuration={300}
          pointsData={[{ lat: TARGET[0], lng: TARGET[1], size: 0.6, color: "#22d3ee" }]}
          pointAltitude="size"
          pointColor="color"
          pointRadius={0.4}
        />
      </div>
      <div className="flex justify-center gap-4 mt-1">
        {Object.entries(ARC_COLORS).map(([type, color]) => (
          <div key={type} className="flex items-center gap-1.5 text-xs text-slate-400">
            <div className="w-2 h-2 rounded-full" style={{ background: color }} />
            {type}
          </div>
        ))}
      </div>
    </div>
  );
}
