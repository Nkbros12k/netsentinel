"""ML model loading and inference."""

import json
import os

import joblib
import numpy as np

from config import MODEL_DIR

_model = None
_scaler = None
_encoders = {}
_feature_names = []
_class_names = []


def _load():
    global _model, _scaler, _encoders, _feature_names, _class_names

    _model = joblib.load(os.path.join(MODEL_DIR, "model.joblib"))
    _scaler = joblib.load(os.path.join(MODEL_DIR, "scaler.joblib"))

    with open(os.path.join(MODEL_DIR, "feature_names.json")) as f:
        _feature_names = json.load(f)

    for fname in os.listdir(MODEL_DIR):
        if fname.startswith("encoder_") and fname.endswith(".joblib"):
            name = fname.replace("encoder_", "").replace(".joblib", "")
            _encoders[name] = joblib.load(os.path.join(MODEL_DIR, fname))

    _class_names = list(_encoders["target"].classes_)


def ensure_loaded():
    if _model is None:
        _load()


def predict(flow_dict: dict) -> dict:
    ensure_loaded()

    categorical = {"protocol_type", "service", "flag"}
    features = []
    for col in _feature_names:
        val = flow_dict.get(col, 0)
        if col in categorical:
            enc = _encoders.get(col)
            if enc is not None and val in enc.classes_:
                val = enc.transform([val])[0]
            else:
                val = 0
        features.append(float(val))

    X = np.array([features], dtype=np.float32)
    X = _scaler.transform(X)

    proba = _model.predict_proba(X)[0]
    pred_idx = int(np.argmax(proba))
    confidence = float(proba[pred_idx])
    prediction = _class_names[pred_idx]

    if prediction == "Normal":
        threat_level = "none"
    elif confidence < 0.5:
        threat_level = "low"
    elif confidence < 0.75:
        threat_level = "medium"
    elif confidence < 0.9:
        threat_level = "high"
    else:
        threat_level = "critical"

    return {
        "prediction": prediction,
        "confidence": confidence,
        "threat_level": threat_level,
        "attack_type": prediction,
    }


def is_ready() -> bool:
    try:
        ensure_loaded()
        return _model is not None
    except Exception:
        return False
