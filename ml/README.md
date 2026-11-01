# ShopFlow ML Engineering

Directory tree:
```
ml/
├── datasets/
│   ├── olist/              # Brazilian Olist e-commerce dataset (read-only, historical ML data)
│   └── synthetic/          # Explicitly identified synthetic demonstration records
├── features/
├── pipelines/
├── models/
├── training/
├── evaluation/
├── inference/
├── registry/
├── monitoring/
├── explainability/
├── pyproject.toml
├── requirements.txt
└── README.md
```

ML engineering principles (per VISION.md §4):

- Training, experimentation, inference, and business integration remain distinct.
- Models accept validated features and return predictions; they know nothing about HTTP or React.
- The application layer integrates ML capabilities into order management via APIs.
- Reproducible experiments, feature pipelines, temporal validation, hyperparameter tuning,
  model evaluation, explainability, versioning, and inference.
- Primary dataset: Brazilian Olist e-commerce dataset (historical, separate from live Postgres data).

Dataset strategy (per VISION.md §5):
- Historical data used for ML training → `ml/datasets/olist/`
- Live marketplace data stored in PostgreSQL (backend)
- Application seed data
- Synthetic demonstration records, explicitly identified → `ml/datasets/synthetic/`

Historical transactions must not be treated as live inventory or real-time marketplace activity.
