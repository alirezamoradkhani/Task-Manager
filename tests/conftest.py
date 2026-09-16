import os
from uuid import uuid4

os.environ["MONGODB_URL"] = os.getenv("TEST_MONGODB_URL", "mongodb://localhost:27017")

import pytest
from fastapi.testclient import TestClient
from pymongo import MongoClient
from app.main import app
from app import database
from app.tasks import router
from app.tasks.repository import TaskRepository


@pytest.fixture
def mongo_collection():
    uri = os.getenv("TEST_MONGODB_URL")
    if not uri:
        pytest.skip("Set TEST_MONGODB_URL to run tests against a real MongoDB")
    mongo = MongoClient(uri, serverSelectionTimeoutMS=5000, tz_aware=True)
    database_name = f"task_manager_test_{uuid4().hex}"
    try:
        mongo.admin.command("ping")
        yield mongo[database_name]["tasks"]
    finally:
        try:
            mongo.drop_database(database_name)
        finally:
            mongo.close()


@pytest.fixture
def client(mongo_collection, monkeypatch):
    repository = TaskRepository(collection=mongo_collection)
    app.dependency_overrides[router.get_task_repository] = lambda: repository
    monkeypatch.setattr(database, "client", mongo_collection.database.client)
    try:
        with TestClient(app) as test_client:
            yield test_client
    finally:
        app.dependency_overrides.pop(router.get_task_repository, None)
