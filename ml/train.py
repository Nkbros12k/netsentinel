"""Train XGBoost model on NSL-KDD dataset."""

import os
import joblib
import numpy as np
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from xgboost import XGBClassifier
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns

from download_data import download
from feature_engineering import load_raw, preprocess, save_artifacts

ML_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(ML_DIR, "data")
MODEL_DIR = os.path.join(ML_DIR, "model")
DOCS_DIR = os.path.join(ML_DIR, "..", "docs")


def train():
    download()

    print("\n[1/5] Loading data...")
    train_df = load_raw(os.path.join(DATA_DIR, "KDDTrain+.txt"))
    test_df = load_raw(os.path.join(DATA_DIR, "KDDTest+.txt"))
    print(f"  Train: {len(train_df):,} samples")
    print(f"  Test:  {len(test_df):,} samples")

    print("\n[2/5] Preprocessing...")
    X_train, y_train, feature_names, encoders, scaler = preprocess(train_df, fit=True)
    X_test, y_test, _, _, _ = preprocess(test_df, encoders=encoders, scaler=scaler, fit=False)
    print(f"  Features: {len(feature_names)}")
    print(f"  Classes:  {list(encoders['target'].classes_)}")

    print("\n[3/5] Training XGBoost...")
    model = XGBClassifier(
        n_estimators=200,
        max_depth=8,
        learning_rate=0.1,
        objective="multi:softprob",
        num_class=len(encoders["target"].classes_),
        eval_metric="mlogloss",
        random_state=42,
        n_jobs=-1,
        verbosity=0,
    )
    model.fit(X_train, y_train)
    print("  Training complete.")

    print("\n[4/5] Evaluating...")
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    class_names = list(encoders["target"].classes_)
    report = classification_report(y_test, y_pred, target_names=class_names)
    print(f"  Accuracy: {acc:.4f}")
    print(f"\n{report}")

    print("\n[5/5] Saving artifacts...")
    os.makedirs(MODEL_DIR, exist_ok=True)
    os.makedirs(DOCS_DIR, exist_ok=True)
    joblib.dump(model, os.path.join(MODEL_DIR, "model.joblib"))
    save_artifacts(encoders, scaler, feature_names, MODEL_DIR)

    # Confusion matrix
    cm = confusion_matrix(y_test, y_pred)
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", xticklabels=class_names, yticklabels=class_names, ax=ax)
    ax.set_xlabel("Predicted")
    ax.set_ylabel("Actual")
    ax.set_title(f"Confusion Matrix (Accuracy: {acc:.1%})")
    plt.tight_layout()
    fig.savefig(os.path.join(DOCS_DIR, "confusion-matrix.png"), dpi=150)
    plt.close()

    # Feature importance
    importances = model.feature_importances_
    top_idx = np.argsort(importances)[-15:]
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.barh([feature_names[i] for i in top_idx], importances[top_idx], color="#22d3ee")
    ax.set_xlabel("Importance")
    ax.set_title("Top 15 Feature Importances")
    plt.tight_layout()
    fig.savefig(os.path.join(DOCS_DIR, "feature-importance.png"), dpi=150)
    plt.close()

    print(f"\n  Model saved to {MODEL_DIR}")
    print(f"  Plots saved to {DOCS_DIR}")
    print(f"\n  Accuracy: {acc:.1%}")


if __name__ == "__main__":
    train()
