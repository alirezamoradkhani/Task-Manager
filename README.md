# Task Manager API

An educational task manager built with FastAPI and MongoDB using PyMongo.

## Project structure

```text
app/
  main.py              # FastAPI application and health checks
  config.py            # Environment settings
  database.py          # MongoDB client and tasks collection
  tasks/
    router.py          # HTTP endpoints at /tasks
    service.py         # Application rules and not-found handling
    repository.py      # MongoDB queries and document writes
    schema.py          # Request validation and response models
```

A request follows `router → service → repository → MongoDB`. The response
converts MongoDB documents into the `TaskRead` schema. Task IDs are MongoDB
`ObjectId` values represented as strings in the API.

## Requirements

- Python 3.12+ for local development
- MongoDB locally, in Docker, or on MongoDB Atlas
- Docker Compose if running the entire application in containers

## Run with Docker Compose

```bash
docker compose up --build
```

Compose starts MongoDB and the API. The API waits for MongoDB to be healthy.
MongoDB data is stored in the `mongo_data` volume, and its port is exposed only
on localhost. The API connects to `mongodb://mongo:27017` inside the Compose
network.

The API is available at <http://localhost:8000>, with Swagger UI at
<http://localhost:8000/docs>.

Stop the containers when finished to release CPU and memory:

```bash
docker compose down
```

The database volume is kept so your tasks remain available the next time.

## Run locally

Create your environment settings:

```bash
cp .env.example .env
```

```env
MONGODB_URL=mongodb://localhost:27017
MONGODB_DATABASE=task_manager
```

For MongoDB Atlas, use its connection string as `MONGODB_URL`. Do not commit
`.env` or share credentials. These settings apply to local runs; Compose uses
its own MongoDB service.

You can run just MongoDB with Docker:

```bash
docker compose up -d mongo
```

Then start the API locally:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
uvicorn app.main:app --reload
```

MongoDB creates the database and collection on the first write. Stop the
local API with Ctrl+C and run `docker compose down` when finished.

## Endpoints

| Method | Path | Purpose |
| --- | --- | --- |
| `POST` | `/tasks` | Create a task |
| `GET` | `/tasks` | List tasks by importance, then creation time, descending |
| `GET` | `/tasks/{id}` | Get one task |
| `PATCH` | `/tasks/{id}` | Edit or complete a task |
| `DELETE` | `/tasks/{id}` | Delete a task |
| `GET` | `/health` | API health check |
| `GET` | `/health/mongodb` | MongoDB connectivity check |

Listing accepts `offset` (default 0) and `limit` (default 50, maximum 100).
For `PATCH`, omit fields to keep their existing values. Explicit `null` values
are rejected with HTTP 422. Missing or invalid task IDs return HTTP 404.
MongoDB connection failures return HTTP 503; `/health/mongodb` also returns
HTTP 503 when MongoDB is unavailable.

Create a task:

```bash
curl -X POST http://localhost:8000/tasks \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Learn MongoDB",
    "description": "Practice document CRUD",
    "importance": 5
  }'
```

## Tests

```bash
python -m pytest
```

Integration tests use a real MongoDB and are skipped unless `TEST_MONGODB_URL`
is set. Tests create uniquely named temporary databases and remove them
afterwards. The test user needs permission to create and drop these databases.

To run all tests with a dedicated temporary MongoDB, run this block in Bash
with your virtual environment activated:

```bash
(
  set -e
  docker run -d --rm --name task-manager-mongo-test \
    -p 127.0.0.1:27028:27017 mongo:8
  trap 'docker stop task-manager-mongo-test' EXIT
  TEST_MONGODB_URL=mongodb://127.0.0.1:27028 python -m pytest
)
```

The temporary container is stopped and removed when the block finishes,
including when a test fails.
