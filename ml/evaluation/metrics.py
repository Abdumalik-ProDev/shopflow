"""ML evaluation utilities."""

from __future__ import annotations

from typing import Any, Dict

from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score, accuracy_score


def regression_metrics(y_true, y_pred) -> Dict[str, float]:
    return {
        "mae": float(mean_absolute_error(y_true, y_pred)),
        "rmse": float(mean_squared_error(y_true, y_pred, squared=False)),
        "r2": float(r2_score(y_true, y_pred)),
    }


def classification_metrics(y_true, y_pred) -> Dict[str, float]:
    return {"accuracy": float(accuracy_score(y_true, y_pred))}


__all__ = ["regression_metrics", "classification_metrics"]
