"""Training entry points for all ML pipelines."""

from __future__ import annotations

import mlflow

from ml.pipelines.delivery_eta_pipeline import train_delivery_eta
from ml.pipelines.demand_forecasting_pipeline import train_demand_forecast
from ml.pipelines.recommendation_pipeline import train_recommendation_model


def main() -> None:
    with mlflow.start_run(run_name="delivery_eta_training"):
        result = train_delivery_eta()
        print("Delivery ETA:", result)

    with mlflow.start_run(run_name="demand_forecast_training"):
        result = train_demand_forecast()
        print("Demand Forecast:", result)

    with mlflow.start_run(run_name="recommendation_training"):
        result = train_recommendation_model()
        print("Recommendations:", result)


if __name__ == "__main__":
    main()
