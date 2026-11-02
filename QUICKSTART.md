# ShopFlow Quickstart

## 1. Backend

```bash
cd backend
uv sync
cp .env.example .env
uv run pytest
uv run uvicorn app.main:app --reload
```

Swagger API Docs: http://localhost:8000/docs  
Health Check: http://localhost:8000/health

## 2. Frontend

```bash
cd frontend
npm install
npm test -- --run
npm run dev
```

App: http://localhost:5173

## 3. ML Pipelines

```bash
cd ml
uv sync
uv run python data/clean_data.py
uv run python -m training.train_all
```

## 4. Full Stack via Docker

```bash
docker compose -f docker/docker-compose.yml up --build
```
