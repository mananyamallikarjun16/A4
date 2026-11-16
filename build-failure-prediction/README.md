# Build-Failure Prediction

This project trains a scikit-learn logistic-regression classifier on historical
build records. Numeric fields are standardized, branch names are one-hot
encoded, and the model reports evaluation accuracy and ROC AUC. A separate
example build receives a failure probability and a Low/Medium/High risk label.

## Setup, tests, and prediction

Requires Python 3.10+.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m pytest -v
python scripts\predict_build.py data\historical_builds.csv
python scripts\predict_build.py data\historical_builds.csv --json
```

The included CSV is a small illustrative dataset, not a production-quality
benchmark. It contains numeric build attributes, a categorical branch feature,
and the binary `failed` target. Real deployment should use representative,
time-ordered build history and evaluate for class imbalance and data leakage.

## Important files

- `buildpredict/model.py` validates input columns, preprocesses numeric and
  categorical features, trains the classifier, calculates metrics and
  probabilities, classifies risk, and can save/load a model artifact.
- `data/historical_builds.csv` is the sample historical dataset.
- `scripts/predict_build.py` trains, evaluates, then predicts one future example.
- `tests/test_model.py` checks training, evaluation, prediction and validation.
- `.github/workflows/ci.yml` installs Python 3.12 dependencies, runs tests, and
  executes the sample prediction on pushes and pull requests.

Risk cutoffs are `<0.30` Low, `0.30–<0.65` Medium, and `>=0.65` High. They are
demonstration thresholds; teams should calibrate them against their operational
costs and validation data.

## GitHub Actions and intentional failure

The CI workflow runs pytest and the prediction command. Temporarily alter an
expected value in a test, commit and push, then inspect
**Actions → Python CI → failed run → test** for the red check and traceback.
Restore the expectation and push a new commit; the latest passing run will
display a green check. The sample dataset and all checks run offline.

## Publish

The public repository is available at
https://github.com/mananyamallikarjun16/build-failure-prediction. The remote is
configured locally; push the main branch with:

```powershell
git push -u origin main
```
