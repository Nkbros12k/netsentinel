# NetSentinel -- Real-Time Network Threat Detection

![Python](https://img.shields.io/badge/Python-3.11-blue?style=flat-square&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?style=flat-square&logo=fastapi)
![React](https://img.shields.io/badge/React-18-61DAFB?style=flat-square&logo=react)
![XGBoost](https://img.shields.io/badge/XGBoost-2.1-orange?style=flat-square)
![Kubernetes](https://img.shields.io/badge/Kubernetes-Ready-326CE5?style=flat-square&logo=kubernetes)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?style=flat-square&logo=docker)

ML-powered network intrusion detection system with a real-time dashboard, 3D threat globe, auto-scaling Kubernetes deployment, and simulated traffic generation.

---

## Architecture

```
                    +------------------+
                    |   Simulator      |
                    |  (Traffic Gen)   |
                    +--------+---------+
                             |
                     POST /predict
                             |
                    +--------v---------+
                    |   FastAPI API     |
                    |  XGBoost Model    |
                    |  WebSocket Push   |
                    +----+--------+----+
                         |        |
                    GET /stats   WS /ws/threats
                         |        |
                    +----v--------v----+
                    |  React Dashboard  |
                    |  3D Globe + Charts |
                    |  Live Threat Feed  |
                    +-------------------+
```

**Data Flow:** The simulator generates mixed normal and attack network traffic (based on NSL-KDD distributions), sends each flow to the API for classification, and the API broadcasts detected threats via WebSocket to all connected dashboards in real-time.

---

## ML Model

**Dataset:** NSL-KDD (125,973 training samples, 22,544 test samples)

**Model:** XGBoost multi-class classifier (5 classes)

**Classes:**
| Class | Description | Training Samples |
|-------|-------------|-----------------|
| Normal | Legitimate traffic | 67,343 |
| DoS | Denial of Service (neptune, smurf, back, etc.) | 45,927 |
| Probe | Reconnaissance (portsweep, nmap, satan, etc.) | 11,656 |
| R2L | Remote to Local (guess_passwd, ftp_write, etc.) | 995 |
| U2R | User to Root (buffer_overflow, rootkit, etc.) | 52 |

**Performance:**
- Accuracy: 77% (NSL-KDD test set is intentionally adversarial)
- DoS Precision: 96%
- Normal Recall: 97%

**Feature Engineering:**
- 41 features per network flow (duration, bytes, flags, error rates, host-based stats)
- Categorical encoding for protocol_type, service, flag
- StandardScaler normalization
- Top features: service type, flag, src/dst bytes, error rates, connection counts

**Why XGBoost over deep learning:** For tabular network traffic data, gradient boosted trees consistently match or outperform neural networks while training in seconds and producing interpretable feature importances. The model file is ~1MB vs hundreds of MB for a comparable neural network.

---

## Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| ML Training | XGBoost, scikit-learn, Pandas | Model training and evaluation |
| API | FastAPI, Uvicorn | Prediction serving + WebSocket |
| Dashboard | React 18, TypeScript, Vite | Real-time visualization |
| Charts | Recharts | Threat timeline, attack distribution |
| 3D Globe | react-globe.gl, Three.js | Animated global threat map with attack arcs |
| Styling | Tailwind CSS | Dark-themed responsive UI |
| Containers | Docker, docker-compose | Local deployment |
| Orchestration | Kubernetes | Production deployment with HPA auto-scaling |

---

## Quick Start

### Local (without Docker)

```bash
# 1. Train the model
cd ml
pip install -r requirements.txt
python train.py

# 2. Start the API
cd ../api
pip install -r requirements.txt
uvicorn main:app --port 8000

# 3. Start the dashboard (new terminal)
cd ../dashboard
npm install
npm run dev

# 4. Start the simulator (new terminal)
cd ../simulator
pip install -r requirements.txt
python simulator.py
```

Open http://localhost:5173 -- the dashboard will show threats in real-time.

### Docker Compose

```bash
docker compose up --build
```

Open http://localhost:3000

### Kubernetes

```bash
# Build images
docker build -t netsentinel-api -f api/Dockerfile .
docker build -t netsentinel-dashboard dashboard/
docker build -t netsentinel-simulator simulator/

# Deploy
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/api/
kubectl apply -f k8s/dashboard/
kubectl apply -f k8s/simulator/

# Access dashboard
minikube service dashboard-service -n netsentinel
```

---

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/predict` | Classify a single network flow |
| `POST` | `/predict/batch` | Classify multiple flows |
| `GET` | `/stats` | Aggregated detection statistics |
| `GET` | `/recent` | Last 50 threat detections |
| `GET` | `/health` | Liveness probe |
| `GET` | `/ready` | Readiness probe (model loaded) |
| `WS` | `/ws/threats` | Real-time threat stream |

**Example request:**
```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"duration": 0, "protocol_type": "tcp", "service": "http", "flag": "S0", "src_bytes": 0, "dst_bytes": 0, "count": 500, "serror_rate": 1.0, "srv_serror_rate": 1.0}'
```

**Example response:**
```json
{
  "prediction": "DoS",
  "confidence": 0.94,
  "threat_level": "critical",
  "timestamp": "2026-04-07T23:15:00Z",
  "attack_type": "DoS"
}
```

---

## Kubernetes Architecture

- **API Deployment**: 2 replicas with HPA (scales to 10 based on CPU/memory)
- **Dashboard Deployment**: 1 replica with nginx reverse proxy
- **Simulator Deployment**: 1 replica generating continuous traffic
- **Health Checks**: Liveness (`/health`) and readiness (`/ready`) probes on API pods
- **ConfigMap**: Centralized configuration for model path, simulator rate, attack ratio
- **HPA**: Scales API pods at 70% CPU utilization, ensuring low-latency predictions under load

---

## Dashboard Features

- **3D Threat Globe**: Interactive, spinnable globe showing attack arcs from source cities to target (Austin, TX) with color-coded attack types
- **Stats Cards**: Total processed, threats detected, threats/min, uptime
- **Threat Timeline**: Stacked area chart showing attack types over time
- **Attack Distribution**: Donut chart breaking down attack categories
- **Live Threat Feed**: Scrolling list with confidence bars, severity badges, and timestamps
- **WebSocket**: Real-time push updates -- no polling delay

---

## Project Structure

```
netsentinel/
├── ml/                          # ML training pipeline
│   ├── train.py                 # XGBoost training + evaluation
│   ├── feature_engineering.py   # Preprocessing + encoding
│   ├── download_data.py         # NSL-KDD dataset download
│   └── model/                   # Saved model artifacts
├── api/                         # FastAPI backend
│   ├── main.py                  # App entry point
│   ├── routers/                 # Endpoint handlers
│   │   ├── predict.py           # Prediction + WebSocket
│   │   ├── stats.py             # Statistics
│   │   └── health.py            # Health checks
│   ├── services/                # Business logic
│   │   ├── predictor.py         # Model inference
│   │   └── threat_store.py      # In-memory event buffer
│   └── models/schemas.py        # Pydantic models
├── simulator/                   # Traffic generator
│   ├── simulator.py             # Main loop
│   └── profiles.py              # Attack distributions
├── dashboard/                   # React frontend
│   └── src/
│       ├── components/          # UI components
│       │   ├── ThreatGlobe.tsx  # 3D globe visualization
│       │   ├── ThreatFeed.tsx   # Live event feed
│       │   ├── ThreatChart.tsx  # Timeline chart
│       │   ├── AttackTypesPie.tsx
│       │   ├── StatsCards.tsx
│       │   └── Header.tsx
│       └── hooks/               # WebSocket + polling
├── k8s/                         # Kubernetes manifests
│   ├── api/                     # API deployment + HPA
│   ├── dashboard/               # Dashboard deployment
│   └── simulator/               # Simulator deployment
├── docker-compose.yml           # Local orchestration
└── docs/                        # Generated plots
```

---

## Technical Decisions

**In-memory threat store vs. database**: Uses a `deque` ring buffer (last 1000 events) to keep the stack simple and avoid external dependencies. Production would use Redis Streams or TimescaleDB for persistence and horizontal scaling across API replicas.

**WebSocket vs. SSE**: WebSocket enables bidirectional communication and has first-class FastAPI support. This allows future features like dashboard-to-API commands (pause/resume, filter adjustments).

**Simulated traffic vs. pcap replay**: A custom simulator is portable, requires no elevated permissions, and immediately demonstrates the system end-to-end. Production would integrate with network taps, NetFlow/sFlow collectors, or Zeek/Suricata output.

**HPA scaling strategy**: Scales on CPU (70% threshold) because model inference is CPU-bound. Memory scaling (80%) acts as a safety net. In production, custom metrics (prediction latency p99) would be more appropriate.

---

## License

MIT
