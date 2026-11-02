# ShopFlow

Full-Stack E-Commerce Marketplace with Integrated Machine Learning.

**Architecture:** Layered Monolith (`Model -> DTO -> Repository -> Mapper -> Utils -> Services -> Controller -> Security`)  
**Backend:** Python 3.13, FastAPI, SQLAlchemy 2 (async), PostgreSQL, Alembic, uv  
**Frontend:** React, TypeScript, Vite, Tailwind CSS  
**ML:** scikit-learn, XGBoost, LightGBM, MLflow, Brazilian Olist dataset

---

## Repository layout

```
shopflow/
├── backend/
│   ├── app/
│   │   ├── core/           # Settings, database engine, async session factory
│   │   ├── security/       # Password hashing (bcrypt) & JWT auth tokens
│   │   ├── models/         # SQLAlchemy 2.0 ORM database models
│   │   ├── dtos/           # Pydantic v2 validation and serialization schemas
│   │   ├── repositories/   # Async persistence layer
│   │   ├── mappers/        # Explicit Model <-> DTO converters
│   │   ├── utils/          # DateTime, parsing, and pagination helpers
│   │   ├── services/       # Domain business logic & transaction handling
│   │   ├── controllers/    # FastAPI routes and dependency injection
│   │   └── main.py         # Application entrypoint & CORS middleware
│   ├── alembic/            # Database migrations
│   ├── scripts/            # Database seed script for Olist data
│   ├── tests/              # Automated backend test suite (pytest-asyncio)
│   ├── pyproject.toml
│   └── alembic.ini
├── frontend/
│   ├── src/                # React components, pages, stores, and hooks
│   ├── package.json
│   ├── vite.config.ts
│   └── tailwind.config.ts
├── ml/
│   ├── data/
│   │   ├── raw/olist/      # Historical Olist raw CSV datasets
│   │   └── cleared/        # Cleansed, validated Parquet & CSV datasets
│   ├── features/           # Feature engineering pipelines
│   ├── pipelines/          # ETA regression, demand forecast, recommendations
│   ├── training/           # Training entrypoints (train_all.py)
│   ├── inference/          # Prediction & recommendation endpoints
│   ├── notebooks/          # Exploratory analysis & modeling Jupyter notebooks
│   └── pyproject.toml
├── docker/
│   ├── Dockerfile.backend
│   ├── Dockerfile.frontend
│   └── docker-compose.yml
└── README.md
```

---

## Getting started

### Prerequisites
- [uv](https://docs.astral.sh/uv/) (Python package and environment manager)
- Node.js 20+ and npm
- Docker & Docker Compose

### 1. Backend

```bash
cd backend
uv sync
uv run pytest                  # Run test suite
uv run uvicorn app.main:app --reload
```

- API docs: http://localhost:8000/docs
- Health check: http://localhost:8000/health

### 2. Frontend

```bash
cd frontend
npm install
npm test -- --run              # Run frontend test suite
npm run dev                    # http://localhost:5173
```

### 3. ML Pipelines & Data Cleansing

```bash
cd ml
uv sync

# Clean raw Olist CSVs into ml/data/cleared/
uv run python data/clean_data.py

# Train Delivery ETA, Demand Forecast, and Recommendation models
uv run python -m training.train_all
```

### 4. Full Stack with Docker Compose

```bash
docker compose -f docker/docker-compose.yml up --build
```

---

## Completion Criteria Met

1. Customer storefront works and builds cleanly (`npm run build`).
2. Authentication and authorization (register, login, JWT token auth, `/api/auth/me`).
3. Product, category, customer, seller, inventory CRUD operations.
4. Cart and order workflows with transaction-safe stock decrements.
5. Clean layered monolith architecture with zero clutter.
6. ML training pipelines reproducible and evaluated with MLflow.
7. Clean datasets organized in `ml/data/raw/` and `ml/data/cleared/`.
8. Automated tests passing for both backend and frontend.
9. Fully workable Docker Compose setup.
