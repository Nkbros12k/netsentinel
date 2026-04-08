import { Header } from "./components/Header";
import { StatsCards } from "./components/StatsCards";
import { ThreatChart } from "./components/ThreatChart";
import { AttackTypesPie } from "./components/AttackTypesPie";
import { ThreatFeed } from "./components/ThreatFeed";
import { ThreatGlobe } from "./components/ThreatGlobe";
import { useWebSocket } from "./hooks/useWebSocket";
import { useStats } from "./hooks/useStats";

const WS_URL = `${window.location.protocol === "https:" ? "wss:" : "ws:"}//${window.location.host}/ws/threats`;

function App() {
  const { events, connected } = useWebSocket(WS_URL);
  const stats = useStats(3000);

  return (
    <div className="min-h-screen bg-[#0a0e1a]">
      <Header connected={connected} />
      <main className="max-w-7xl mx-auto px-4 py-5 space-y-4">
        <StatsCards stats={stats} />

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
          <ThreatGlobe events={events} />
          <div className="space-y-4">
            <ThreatChart events={events} />
            <AttackTypesPie breakdown={stats.attack_breakdown} />
          </div>
        </div>

        <ThreatFeed events={events} />
      </main>
    </div>
  );
}

export default App;
