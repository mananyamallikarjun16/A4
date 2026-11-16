from pathlib import Path

import pytest

from buildpredict.model import load_dataset, predict_risk, train_and_evaluate

ROOT = Path(__file__).resolve().parents[1]


def test_sample_dataset_trains_evaluates_and_predicts() -> None:
    frame = load_dataset(ROOT / "data" / "historical_builds.csv")
    model, metrics = train_and_evaluate(frame)
    prediction = predict_risk(
        model,
        {
            "changed_files": 8,
            "tests_run": 140,
            "avg_test_seconds": 1.8,
            "flaky_tests": 2,
            "recent_failure_rate": 0.45,
            "dependencies_changed": 1,
            "branch": "new-branch",
        },
    )
    assert 0.0 <= prediction["failure_probability"] <= 1.0
    assert prediction["risk"] in {"Low", "Medium", "High"}
    assert 0.0 <= metrics["accuracy"] <= 1.0
    assert 0.0 <= metrics["roc_auc"] <= 1.0


def test_dataset_requires_expected_columns(tmp_path: Path) -> None:
    dataset = tmp_path / "bad.csv"
    dataset.write_text("branch,failed\nmain,0\n", encoding="utf-8")
    with pytest.raises(ValueError, match="missing required columns"):
        load_dataset(dataset)
