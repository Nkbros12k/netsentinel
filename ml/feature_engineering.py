"""Feature engineering for NSL-KDD network traffic data."""

import json
import os

import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder, StandardScaler

COLUMN_NAMES = [
    "duration", "protocol_type", "service", "flag", "src_bytes", "dst_bytes",
    "land", "wrong_fragment", "urgent", "hot", "num_failed_logins", "logged_in",
    "num_compromised", "root_shell", "su_attempted", "num_root",
    "num_file_creations", "num_shells", "num_access_files", "num_outbound_cmds",
    "is_host_login", "is_guest_login", "count", "srv_count", "serror_rate",
    "srv_serror_rate", "rerror_rate", "srv_rerror_rate", "same_srv_rate",
    "diff_srv_rate", "srv_diff_host_rate", "dst_host_count", "dst_host_srv_count",
    "dst_host_same_srv_rate", "dst_host_diff_srv_rate", "dst_host_same_src_port_rate",
    "dst_host_srv_diff_host_rate", "dst_host_serror_rate", "dst_host_srv_serror_rate",
    "dst_host_rerror_rate", "dst_host_srv_rerror_rate", "label", "difficulty",
]

CATEGORICAL_COLS = ["protocol_type", "service", "flag"]

ATTACK_MAP = {
    "normal": "Normal",
    "neptune": "DoS", "smurf": "DoS", "back": "DoS", "teardrop": "DoS",
    "pod": "DoS", "land": "DoS", "apache2": "DoS", "udpstorm": "DoS",
    "processtable": "DoS", "mailbomb": "DoS",
    "satan": "Probe", "ipsweep": "Probe", "portsweep": "Probe", "nmap": "Probe",
    "mscan": "Probe", "saint": "Probe",
    "warezclient": "R2L", "guess_passwd": "R2L", "warezmaster": "R2L",
    "imap": "R2L", "ftp_write": "R2L", "multihop": "R2L", "phf": "R2L",
    "spy": "R2L", "named": "R2L", "snmpgetattack": "R2L", "xlock": "R2L",
    "xsnoop": "R2L", "sendmail": "R2L", "httptunnel": "R2L",
    "snmpguess": "R2L", "worm": "R2L",
    "buffer_overflow": "U2R", "rootkit": "U2R", "loadmodule": "U2R",
    "perl": "U2R", "sqlattack": "U2R", "xterm": "U2R", "ps": "U2R",
}


def load_raw(filepath: str) -> pd.DataFrame:
    df = pd.read_csv(filepath, header=None, names=COLUMN_NAMES)
    df["label"] = df["label"].str.strip().str.lower()
    df["attack_category"] = df["label"].map(ATTACK_MAP).fillna("Unknown")
    df.drop(columns=["difficulty"], inplace=True)
    return df


def preprocess(
    df: pd.DataFrame,
    encoders: dict | None = None,
    scaler: StandardScaler | None = None,
    fit: bool = True,
):
    if encoders is None:
        encoders = {}

    for col in CATEGORICAL_COLS:
        if fit:
            le = LabelEncoder()
            df[col] = le.fit_transform(df[col].astype(str))
            encoders[col] = le
        else:
            le = encoders[col]
            df[col] = df[col].astype(str).map(
                lambda x, _le=le: _le.transform([x])[0]
                if x in _le.classes_
                else -1
            )

    target_le = encoders.get("target")
    if fit:
        target_le = LabelEncoder()
        df["target"] = target_le.fit_transform(df["attack_category"])
        encoders["target"] = target_le
    else:
        df["target"] = target_le.transform(df["attack_category"])

    feature_cols = [c for c in df.columns if c not in ("label", "attack_category", "target")]
    X = df[feature_cols].values.astype(np.float32)
    y = df["target"].values

    if fit:
        scaler = StandardScaler()
        X = scaler.fit_transform(X)
    else:
        X = scaler.transform(X)

    return X, y, feature_cols, encoders, scaler


def save_artifacts(encoders: dict, scaler: StandardScaler, feature_names: list, model_dir: str):
    os.makedirs(model_dir, exist_ok=True)
    import joblib

    for name, enc in encoders.items():
        joblib.dump(enc, os.path.join(model_dir, f"encoder_{name}.joblib"))
    joblib.dump(scaler, os.path.join(model_dir, "scaler.joblib"))
    with open(os.path.join(model_dir, "feature_names.json"), "w") as f:
        json.dump(feature_names, f)


def load_artifacts(model_dir: str):
    import joblib

    encoders = {}
    for fname in os.listdir(model_dir):
        if fname.startswith("encoder_") and fname.endswith(".joblib"):
            name = fname.replace("encoder_", "").replace(".joblib", "")
            encoders[name] = joblib.load(os.path.join(model_dir, fname))

    scaler = joblib.load(os.path.join(model_dir, "scaler.joblib"))
    with open(os.path.join(model_dir, "feature_names.json")) as f:
        feature_names = json.load(f)

    return encoders, scaler, feature_names
