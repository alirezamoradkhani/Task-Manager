from datetime import datetime, timedelta, timezone
from types import SimpleNamespace

import pytest
from bson import ObjectId
from fastapi.testclient import TestClient
from pymongo import MongoClient
from pymongo.errors import AutoReconnect, ServerSelectionTimeoutError

from app import mongo_database
from app.main import app
from app.tasks import mongo_router
from app.tasks.mongo_repository import MongoTaskRepository


def test_repository_accepts_pymongo_collection():
    with MongoClient("mongodb://localhost:27017", connect=False) as mongo:
        collection = mongo["test"]["tasks"]
        assert MongoTaskRepository(collection).collection is collection


def test_mongo_task_lifecycle(mongo_client, mongo_collection):
    created = mongo_client.post(
        "/mongo/tasks", json={"title": "Ship API", "description": "Details", "importance": 5}
    )
    assert created.status_code == 201
    task = created.json()
    task_id = task["id"]
    assert ObjectId.is_valid(task_id)
    assert task["completed"] is False
    assert mongo_collection.find_one({"_id": ObjectId(task_id)})["title"] == "Ship API"
    fetched = mongo_client.get(f"/mongo/tasks/{task_id}")
    assert fetched.status_code == 200
    assert fetched.json()["title"] == "Ship API"
    updated = mongo_client.patch(
        f"/mongo/tasks/{task_id}", json={"completed": True, "title": "Shipped"}
    )
    assert updated.status_code == 200
    assert updated.json()["completed"] is True
    assert updated.json()["description"] == "Details"
    assert updated.json()["title"] == "Shipped"
    assert datetime.fromisoformat(updated.json()["updated_at"]) >= datetime.fromisoformat(
        fetched.json()["updated_at"]
    )
    assert [item["id"] for item in mongo_client.get("/mongo/tasks").json()] == [task_id]
    deleted = mongo_client.delete(f"/mongo/tasks/{task_id}")
    assert deleted.status_code == 204
    assert deleted.content == b""
    assert mongo_collection.count_documents({}) == 0
    assert mongo_client.get(f"/mongo/tasks/{task_id}").status_code == 404


@pytest.mark.parametrize("field", ["title", "description", "importance", "completed"])
def test_null_update_is_rejected_without_changing_document(mongo_client, mongo_collection, field):
    created = mongo_client.post("/mongo/tasks", json={"title": "Keep valid"}).json()
    before = mongo_collection.find_one({"_id": ObjectId(created["id"])})
    response = mongo_client.patch(f"/mongo/tasks/{created['id']}", json={field: None})
    assert response.status_code == 422
    assert mongo_collection.find_one({"_id": before["_id"]}) == before
    assert mongo_client.get(f"/mongo/tasks/{created['id']}").status_code == 200
    assert mongo_client.get("/mongo/tasks").status_code == 200


def test_empty_update_preserves_document(mongo_client, mongo_collection):
    task_id = mongo_client.post("/mongo/tasks", json={"title": "Unchanged"}).json()["id"]
    before = mongo_collection.find_one({"_id": ObjectId(task_id)})
    assert mongo_client.patch(f"/mongo/tasks/{task_id}", json={}).status_code == 200
    assert mongo_collection.find_one({"_id": before["_id"]}) == before


@pytest.mark.parametrize("method", ["get", "patch", "delete"])
@pytest.mark.parametrize("task_id", ["invalid-id", str(ObjectId())])
def test_missing_or_invalid_task_returns_404(mongo_client, method, task_id):
    kwargs = {"json": {"completed": True}} if method == "patch" else {}
    assert getattr(mongo_client, method)(f"/mongo/tasks/{task_id}", **kwargs).status_code == 404


def test_order_and_pagination(mongo_client, mongo_collection):
    now = datetime.now(timezone.utc)
    for title, importance, age in [("Low", 1, 0), ("Older", 5, 1), ("Newer", 5, 0)]:
        mongo_collection.insert_one({
            "title": title, "description": "", "importance": importance, "completed": False,
            "created_at": now - timedelta(days=age), "updated_at": now,
        })
    assert [task["title"] for task in mongo_client.get("/mongo/tasks").json()] == [
        "Newer", "Older", "Low"
    ]
    response = mongo_client.get("/mongo/tasks", params={"offset": 1, "limit": 1})
    assert [task["title"] for task in response.json()] == ["Older"]


@pytest.mark.parametrize("payload", [{"title": ""}, {"title": "Bad", "importance": 6}])
def test_invalid_create_does_not_write(mongo_client, mongo_collection, payload):
    assert mongo_client.post("/mongo/tasks", json=payload).status_code == 422
    assert mongo_collection.count_documents({}) == 0


def test_live_mongodb_health(mongo_client):
    response = mongo_client.get("/health/mongodb")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_disconnected_mongodb_health(monkeypatch):
    def fail(*args, **kwargs):
        raise ServerSelectionTimeoutError("private connection details")

    monkeypatch.setattr(mongo_database, "client", SimpleNamespace(admin=SimpleNamespace(command=fail)))
    with TestClient(app) as client:
        response = client.get("/health/mongodb")
        assert response.status_code == 503
        assert response.json() == {"status": "unavailable"}
        assert client.get("/health").status_code == 200


@pytest.mark.parametrize("error", [ServerSelectionTimeoutError, AutoReconnect])
@pytest.mark.parametrize("method", ["get", "post", "patch", "delete"])
def test_database_connection_failure_returns_503(monkeypatch, error, method):
    def fail(*args, **kwargs):
        raise error("private connection details")

    service_method = {"get": "list", "post": "create", "patch": "update", "delete": "delete"}[method]
    monkeypatch.setattr(mongo_router.service.repository, service_method, fail)
    path = "/mongo/tasks"
    kwargs = {}
    if method == "post":
        kwargs["json"] = {"title": "Test"}
    elif method in ("patch", "delete"):
        path += f"/{ObjectId()}"
        if method == "patch":
            kwargs["json"] = {"completed": True}
    with TestClient(app) as client:
        response = getattr(client, method)(path, **kwargs)
    assert response.status_code == 503
    assert response.json() == {"detail": "MongoDB is temporarily unavailable"}
