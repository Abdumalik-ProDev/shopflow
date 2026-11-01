# ShopFlow

Full-Stack E-Commerce Marketplace with Integrated Machine Learning.

**Architecture:** Modular Monolith + Domain-Driven Design + Clean Architecture  
**Backend:** Python 3.15, FastAPI, SQLAlchemy 2, PostgreSQL, Alembic, uv  
**Frontend:** React, TypeScript, Vite, Tailwind CSS, Google Stitch UI  
**ML:** scikit-learn, XGBoost, LightGBM, PyTorch, MLflow, Olist dataset

## Repository layout

```
shopflow/
├── backend/
│   ├── pyproject.toml
│   ├── uv.lock
│   ├── .python-version
│   ├── alembic.ini
│   ├── alembic/
│   ├── src/shopflow/
│   ├── notebooks/
│   ├── scripts/
│   ├── tests/
│   └── configs/
├── frontend/
│   ├── package.json
│   ├── vite.config.ts
│   ├── tailwind.config.ts
│   ├── src/
│   └── tests/
├── ml/
│   ├── datasets/
│   ├── features/
│   ├── pipelines/
│   ├── models/
│   ├── training/
│   ├── evaluation/
│   ├── inference/
│   ├── registry/
│   └── monitoring/
├── docker/
│   ├── Dockerfile.backend
│   ├── Dockerfile.frontend
│   └── docker-compose.yml
├── .github/workflows/ci.yml
└── README.md
```

## Getting started

### Prerequisites
- [uv](https://docs.astral.sh/uv/) (Python package management)
- Node.js 20+ and pnpm/npm
- Docker & Docker Compose

### 1. Backend

```bash
cd backend
uv sync
uv run alembic upgrade head
uv run main.py          # or: uvicorn shopflow.main:app --reload
```

API docs: http://localhost:8000/docs

### 2. Frontend

```bash
cd frontend
npm install
npm run dev             # http://localhost:5173
```

### 3. Full stack with Docker Compose

```bash
docker compose -f docker/docker-compose.yml up --build
```

### 4. ML pipelines

```bash
cd ml
pip install -r requirements.txt  # or uv sync
python -m training.train_recommendations
```

## Completion criteria (per VISION.md)

1. Customer storefront works
2. Authentication and authorization work
3. Product, category, customer, seller, inventory CRUD work
4. Cart and order workflows work
5. PostgreSQL persists application data correctly
6. ML pipelines are reproducible and properly evaluated
7. ML predictions accessible through application APIs
8. Frontend consumes the backend successfully
9. Automated tests pass
10. System starts through Docker Compose
11. Documentation allows clone, configure, run, understand
