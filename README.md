# Task Manager API

A small task manager API built with FastAPI. It contains two persistence
implementations so you can compare relational and document databases:

- PostgreSQL with SQLAlchemy and Alembic at `/tasks`
- MongoDB with PyMongo at `/mongo/tasks`

The code uses feature-first boundaries:

- `router.py`: HTTP input and output for PostgreSQL
- `mongo_router.py`: HTTP input and output for MongoDB
- `service.py` / `mongo_service.py`: application rules
- `repository.py` / `mongo_repository.py`: database operations
- `model.py`: SQLAlchemy persistence model
- `schema.py`: API validation and response models

## Requirements

- Python 3.12+
- PostgreSQL (for the original `/tasks` API)
- MongoDB locally or a MongoDB Atlas cluster (for `/mongo/tasks`)

## Environment variables

Copy the example file before running locally:

```bash
cp .env.example .env
```

```env
DATABASE_URL=postgresql+psycopg://task:task@localhost:5432/task_manager
MONGODB_URL=mongodb://localhost:27017
MONGODB_DATABASE=task_manager
```

For MongoDB Atlas, replace `MONGODB_URL` with the connection string provided by
Atlas. Do not commit `.env` or share its credentials.

## Run with Docker Compose

Compose starts the PostgreSQL database and API:

```bash
docker compose up --build
```

The API is available at <http://localhost:8000> and the interactive Swagger UI
at <http://localhost:8000/docs>. PostgreSQL migrations run automatically when
the API container starts.

MongoDB remains optional in this Compose stack. To use MongoDB from the API
container, set `MONGODB_URL` in `.env` to a reachable MongoDB or Atlas URI.

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
alembic upgrade head
uvicorn app.main:app --reload
```

## Endpoints

| Method | PostgreSQL path | MongoDB path | Purpose |
| --- | --- | --- | --- |
| `POST` | `/tasks` | `/mongo/tasks` | Create a task |
| `GET` | `/tasks` | `/mongo/tasks` | List tasks by importance |
| `GET` | `/tasks/{id}` | `/mongo/tasks/{id}` | Get one task |
| `PATCH` | `/tasks/{id}` | `/mongo/tasks/{id}` | Edit or complete a task |
| `DELETE` | `/tasks/{id}` | `/mongo/tasks/{id}` | Delete a task |
| `GET` | `/health` | — | API health check |
| `GET` | `/health/mongodb` | — | MongoDB connectivity check |

MongoDB task IDs are MongoDB `ObjectId` values represented as strings in API
responses. PostgreSQL task IDs remain integers.

Example MongoDB request:

```bash
curl -X POST http://localhost:8000/mongo/tasks \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Learn MongoDB",
    "description": "Practice document CRUD",
    "importance": 5
  }'
```

Check MongoDB connectivity before using its task endpoints:

```bash
curl http://localhost:8000/health/mongodb
```

## Tests

```bash
pytest
```
