"""Training entry points for all ML pipelines."""

from __future__ import annotations

import mlflow

try:
    from pipelines.delivery_eta_pipeline import train_delivery_eta
    from pipelines.demand_forecasting_pipeline import train_demand_forecast
    from pipelines.recommendation_pipeline import train_recommendation_model
except ImportError:
    from ml.pipelines.delivery_eta_pipeline import train_delivery_eta
    from ml.pipelines.demand_forecasting_pipeline import train_demand_forecast
    from ml.pipelines.recommendation_pipeline import train_recommendation_model


def main() -> None:
    print("Running Delivery ETA training pipeline...")
    with mlflow.start_run(run_name="delivery_eta_training"):
        result = train_delivery_eta()
        print("Delivery ETA:", result)

    print("Running Demand Forecast training pipeline...")
    with mlflow.start_run(run_name="demand_forecast_training"):
        result = train_demand_forecast()
        print("Demand Forecast:", result)

    print("Running Recommendation training pipeline...")
    with mlflow.start_run(run_name="recommendation_training"):
        result = train_recommendation_model()
        print("Recommendations:", result)

    print("All ML training pipelines executed successfully.")


if __name__ == "__main__":
    main()
