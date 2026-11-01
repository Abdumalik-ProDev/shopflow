pip install uv

cd backend
uv sync
cp .env.example .env
# edit .env as needed
uv run alembic upgrade head
uv run main.py

# in another terminal
cd frontend
npm install
npm run dev

# or full stack
docker compose -f docker/docker-compose.yml up --build
