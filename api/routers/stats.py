"""Aggregated statistics endpoint."""

from fastapi import APIRouter
from models.schemas import StatsResponse
from services.threat_store import store

router = APIRouter()


@router.get("/stats", response_model=StatsResponse)
async def get_stats():
    return store.get_stats()


@router.get("/recent")
async def get_recent():
    return store.get_recent(50)
