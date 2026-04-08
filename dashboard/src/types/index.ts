export interface ThreatEvent {
  prediction: string;
  confidence: number;
  threat_level: string;
  timestamp: string;
  attack_type: string;
}

export interface Stats {
  total_processed: number;
  threats_detected: number;
  threat_rate: number;
  attack_breakdown: Record<string, number>;
  uptime_seconds: number;
}

export interface ArcData {
  startLat: number;
  startLng: number;
  endLat: number;
  endLng: number;
  color: string;
  attack_type: string;
}
