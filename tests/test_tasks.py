import pytest
from fastapi.testclient import TestClient


def test_task_lifecycle(client: TestClient) -> None:
    created = client.post(
        "/tasks",
        json={"title": "Ship API", "description": "Keep it simple", "importance": 5},
    )
    assert created.status_code == 201
    task_id = created.json()["id"]
    assert created.json()["completed"] is False

    updated = client.patch(f"/tasks/{task_id}", json={"completed": True})
    assert updated.status_code == 200
    assert updated.json()["completed"] is True

    listed = client.get("/tasks")
    assert listed.status_code == 200
    assert [task["id"] for task in listed.json()] == [task_id]

    deleted = client.delete(f"/tasks/{task_id}")
    assert deleted.status_code == 204
    assert client.get(f"/tasks/{task_id}").status_code == 404


def test_validation_and_priority_order(client: TestClient) -> None:
    invalid = client.post("/tasks", json={"title": "Invalid", "importance": 6})
    assert invalid.status_code == 422

    client.post("/tasks", json={"title": "Low", "importance": 1})
    client.post("/tasks", json={"title": "High", "importance": 5})

    response = client.get("/tasks")
    assert [task["title"] for task in response.json()] == ["High", "Low"]


@pytest.mark.parametrize("field", ["title", "description", "importance", "completed"])
def test_null_update_is_rejected(client: TestClient, field: str) -> None:
    created = client.post("/tasks", json={"title": "Keep valid"}).json()
    path = f"/tasks/{created['id']}"
    before = client.get(path).json()
    assert client.patch(path, json={field: None}).status_code == 422
    assert client.get(path).json() == before
