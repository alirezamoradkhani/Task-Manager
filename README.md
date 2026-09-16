# Task Manager API

A small task manager built with FastAPI, PostgreSQL, SQLAlchemy, and Alembic.

The code uses feature-first boundaries inspired by the Bookshop project:

- `router.py`: HTTP input and output
- `service.py`: application rules and use cases
- `repository.py`: database operations
- `model.py`: SQLAlchemy persistence model
- `schema.py`: API validation and response models

## Run with Docker

```bash
docker compose up --build
```

The API is available at <http://localhost:8000> and its interactive Swagger UI at
<http://localhost:8000/docs>. The container applies Alembic migrations before it
starts the API.

## Endpoints

| Method | Path | Purpose |
| --- | --- | --- |
| `POST` | `/tasks` | Create a task |
| `GET` | `/tasks` | List tasks by importance |
| `GET` | `/tasks/{id}` | Get one task |
| `PATCH` | `/tasks/{id}` | Edit or complete a task |
| `DELETE` | `/tasks/{id}` | Delete a task |
| `GET` | `/health` | Container health check |

Example request:

```json
{
  "title": "Finish the API",
  "description": "Keep the architecture simple",
  "importance": 5
}
```

## Run locally

Create a PostgreSQL database, copy `.env.example` to `.env`, update its
`DATABASE_URL` if needed, then run:

```bash
python -m venv venv
pip install -r requirements-dev.txt
alembic upgrade head
uvicorn app.main:app --reload
```

Run tests with:

```bash
pytest
```
