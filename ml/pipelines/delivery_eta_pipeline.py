"""Delivery ETA training pipeline.

Compares statistical baselines, XGBoost, LightGBM, CatBoost per VISION.md §4.
Outputs a trained regressor and logs metrics to MLflow.
"""

from __future__ import annotations

from typing import Any, Dict, Tuple

import mlflow
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

try:
    from xgboost import XGBRegressor  # type: ignore
    HAS_XGB = True
except Exception:  # pragma: no cover
    HAS_XGB = False

try:
    from lightgbm import LGBMRegressor  # type: ignore
    HAS_LGBM = True
except Exception:  # pragma: no cover
    HAS_LGBM = False

from ml.features.build_order_features import build_order_features


def _prepare(df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.Series, list[str]]:
    feature_cols = [
        "item_count", "product_count", "seller_count", "item_price_sum",
        "freight_sum", "payment_value_sum", "payment_types", "review_count",
    ]
    cat_cols = ["order_status"]
    df = df.dropna(subset=["delivery_days"]).copy()
    X = df[feature_cols + cat_cols].copy()
    y = df["delivery_days"].astype(float)
    return X, y, feature_cols + cat_cols


def train_delivery_eta() -> Dict[str, Any]:
    df = build_order_features()
    X, y, cols = _prepare(df)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    numeric = [c for c in cols if c != "order_status"]
    categorical = ["order_status"]

    preprocess = ColumnTransformer(
        transformers=[
            ("num", Pipeline([
                ("imputer", SimpleImputer(strategy="median")),
                ("scaler", StandardScaler()),
            ]), numeric),
            ("cat", Pipeline([
                ("imputer", SimpleImputer(strategy="most_frequent")),
                ("onehot", OneHotEncoder(handle_unknown="ignore")),
            ]), categorical),
        ]
    )

    models: dict[str, Any] = {}
    models["baseline_mean"] = Pipeline([
        ("prep", preprocess),
        ("model", "mean"),  # placeholder replaced below
    ])
    if HAS_XGB:
        models["xgboost"] = Pipeline([
            ("prep", preprocess),
            ("model", XGBRegressor(n_estimators=100, max_depth=6, learning_rate=0.1, random_state=42)),
        ])
    if HAS_LGBM:
        models["lightgbm"] = Pipeline([
            ("prep", preprocess),
            ("model", LGBMRegressor(n_estimators=100, max_depth=6, learning_rate=0.1, random_state=42)),
        ])

    results: dict[str, dict[str, float]] = {}
    best_name = None
    best_mae = float("inf")
    best_model = None

    for name, pipe in models.items():
        if name == "baseline_mean":
            pred = np.full_like(y_test, y_train.mean(), dtype=float)
            mae = mean_absolute_error(y_test, pred)
            rmse = mean_squared_error(y_test, pred, squared=False)
            r2 = r2_score(y_test, pred)
            results[name] = {"mae": mae, "rmse": rmse, "r2": r2}
            continue
        pipe.fit(X_train, y_train)
        pred = pipe.predict(X_test)
        mae = mean_absolute_error(y_test, pred)
        rmse = mean_squared_error(y_test, pred, squared=False)
        r2 = r2_score(y_test, pred)
        results[name] = {"mae": mae, "rmse": rmse, "r2": r2}
        if mae < best_mae:
            best_mae = mae
            best_name = name
            best_model = pipe

    with mlflow.start_run(run_name="delivery_eta"):
        mlflow.log_metrics(results.get(best_name or "baseline_mean", {}))
        mlflow.log_param("best_model", best_name or "baseline_mean")
        if best_model is not None:
            mlflow.sklearn.log_model(best_model, "delivery_eta_model")

    return {"best_model": best_name or "baseline_mean", "metrics": results.get(best_name or "baseline_mean", {})}


__all__ = ["train_delivery_eta"]
