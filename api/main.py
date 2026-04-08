"""NetSentinel API — Real-time network threat detection."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import health, predict, stats
from services.predictor import ensure_loaded

app = FastAPI(
    title="NetSentinel API",
    description="ML-powered network intrusion detection",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router, tags=["Health"])
app.include_router(predict.router, tags=["Prediction"])
app.include_router(stats.router, tags=["Statistics"])


@app.on_event("startup")
async def startup():
    ensure_loaded()
    print("NetSentinel API ready — model loaded.")
