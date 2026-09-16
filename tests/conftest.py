import os
from uuid import uuid4

os.environ["DATABASE_URL"] = "sqlite+pysqlite:///:memory:"
os.environ["MONGODB_URL"] = os.getenv("TEST_MONGODB_URL", "mongodb://localhost:27017")

import pytest
from fastapi.testclient import TestClient
from pymongo import MongoClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
from app.main import app
from app import mongo_database
from app.tasks import mongo_router
from app.tasks.mongo_repository import MongoTaskRepository
from app.tasks.mongo_service import MongoTaskService


@pytest.fixture
def client() -> TestClient:
    engine = create_engine(
        "sqlite+pysqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    testing_session = sessionmaker(bind=engine, expire_on_commit=False)
    Base.metadata.create_all(engine)

    def override_get_db():
        with testing_session() as session:
            yield session

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
    Base.metadata.drop_all(engine)


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
def mongo_client(mongo_collection, monkeypatch):
    repository = MongoTaskRepository(collection=mongo_collection)
    monkeypatch.setattr(mongo_router, "service", MongoTaskService(repository))
    monkeypatch.setattr(mongo_database, "client", mongo_collection.database.client)
    with TestClient(app) as test_client:
        yield test_client
