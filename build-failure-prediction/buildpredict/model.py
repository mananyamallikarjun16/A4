"""Train, evaluate, and use a scikit-learn build-failure classifier."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

TARGET = "failed"
NUMERIC_FEATURES = [
    "changed_files",
    "tests_run",
    "avg_test_seconds",
    "flaky_tests",
    "recent_failure_rate",
    "dependencies_changed",
]
CATEGORICAL_FEATURES = ["branch"]
FEATURES = NUMERIC_FEATURES + CATEGORICAL_FEATURES


def load_dataset(path: str | Path) -> pd.DataFrame:
    frame = pd.read_csv(path)
    required = set(FEATURES + [TARGET])
    missing = required - set(frame.columns)
    if missing:
        raise ValueError(f"Dataset is missing required columns: {', '.join(sorted(missing))}")
    if frame.empty:
        raise ValueError("Dataset must contain at least one build row")
    return frame


def make_pipeline() -> Pipeline:
    preprocess = ColumnTransformer(
        [
            ("numeric", StandardScaler(), NUMERIC_FEATURES),
            ("categorical", OneHotEncoder(handle_unknown="ignore"), CATEGORICAL_FEATURES),
        ]
    )
    return Pipeline(
        [
            ("preprocess", preprocess),
            ("classifier", LogisticRegression(max_iter=1000, class_weight="balanced", random_state=42)),
        ]
    )


def train_and_evaluate(frame: pd.DataFrame, test_size: float = 0.25) -> tuple[Pipeline, dict[str, Any]]:
    if frame[TARGET].nunique() != 2:
        raise ValueError("Training data must include both successful and failed builds")
    features = frame[FEATURES]
    target = frame[TARGET].astype(int)
    x_train, x_test, y_train, y_test = train_test_split(
        features, target, test_size=test_size, random_state=42, stratify=target
    )
    model = make_pipeline()
    model.fit(x_train, y_train)
    probabilities = model.predict_proba(x_test)[:, 1]
    predictions = model.predict(x_test)
    metrics: dict[str, Any] = {
        "accuracy": float(accuracy_score(y_test, predictions)),
        "roc_auc": float(roc_auc_score(y_test, probabilities)),
        "test_rows": int(len(y_test)),
        "classification_report": classification_report(
            y_test, predictions, zero_division=0, output_dict=True
        ),
    }
    return model, metrics


def predict_risk(model: Pipeline, build: dict[str, Any]) -> dict[str, Any]:
    row = pd.DataFrame([{name: build[name] for name in FEATURES}])
    probability = float(model.predict_proba(row)[0, 1])
    risk = "Low" if probability < 0.30 else "Medium" if probability < 0.65 else "High"
    return {"failure_probability": probability, "risk": risk}


def save_model(model: Pipeline, path: str | Path) -> None:
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, destination)


def load_model(path: str | Path) -> Pipeline:
    model = joblib.load(path)
    if not isinstance(model, Pipeline):
        raise TypeError("Saved artifact is not a scikit-learn Pipeline")
    return model
