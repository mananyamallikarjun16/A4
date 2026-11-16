"""Train from historical builds, evaluate, and predict a sample future build."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from buildpredict.model import load_dataset, predict_risk, train_and_evaluate


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("dataset", type=Path)
    parser.add_argument("--json", action="store_true", help="Print machine-readable metrics and prediction")
    args = parser.parse_args()

    frame = load_dataset(args.dataset)
    model, metrics = train_and_evaluate(frame)
    example = {
        "changed_files": 8,
        "tests_run": 140,
        "avg_test_seconds": 1.8,
        "flaky_tests": 2,
        "recent_failure_rate": 0.45,
        "dependencies_changed": 1,
        "branch": "feature",
    }
    prediction = predict_risk(model, example)
    if args.json:
        print(json.dumps({"metrics": metrics, "example_build": example, "prediction": prediction}, indent=2))
    else:
        print(f"Evaluation accuracy: {metrics['accuracy']:.3f}")
        print(f"Evaluation ROC AUC: {metrics['roc_auc']:.3f}")
        print(f"Failure probability: {prediction['failure_probability']:.1%}")
        print(f"Risk: {prediction['risk']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
