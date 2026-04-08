"""Prediction and WebSocket endpoints."""

from datetime import datetime, timezone

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from models.schemas import NetworkFlow, PredictionResponse
from services.predictor import predict
from services.threat_store import store

router = APIRouter()


@router.post("/predict", response_model=PredictionResponse)
async def predict_flow(flow: NetworkFlow):
    result = predict(flow.model_dump())
    result["timestamp"] = datetime.now(timezone.utc)
    await store.add(result)
    return result


@router.post("/predict/batch")
async def predict_batch(flows: list[NetworkFlow]):
    results = []
    for flow in flows:
        result = predict(flow.model_dump())
        result["timestamp"] = datetime.now(timezone.utc)
        await store.add(result)
        results.append(result)
    return results


@router.websocket("/ws/threats")
async def websocket_threats(websocket: WebSocket):
    await websocket.accept()
    store.register_ws(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        store.unregister_ws(websocket)
