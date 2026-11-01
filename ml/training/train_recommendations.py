"""Training entry point: recommendations."""

from __future__ import annotations

import mlflow

from ml.pipelines.recommendation_pipeline import train_recommendation_model


def main() -> None:
    with mlflow.start_run(run_name="recommendations"):
        model, metrics = train_recommendation_model()
        mlflow.log_metrics(metrics)
        mlflow.sklearn.log_model(model, "model")


if __name__ == "__main__":
    main()
