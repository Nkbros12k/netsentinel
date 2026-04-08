"""Health check endpoints."""

from fastapi import APIRouter
from services.predictor import is_ready

router = APIRouter()


@router.get("/health")
async def health():
    return {"status": "healthy"}


@router.get("/ready")
async def ready():
    if is_ready():
        return {"status": "ready", "model_loaded": True}
    return {"status": "not_ready", "model_loaded": False}
