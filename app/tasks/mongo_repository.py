from datetime import datetime, timezone
from typing import Any

from bson import ObjectId
from pymongo.collection import Collection
from pymongo.results import InsertOneResult

from app.mongo_database import tasks_collection
from app.tasks.schema import MongoTaskRead, TaskCreate, TaskUpdate


class MongoTaskRepository:
    """MongoDB persistence operations for tasks."""

    def __init__(self, collection: Collection[Any] | None = None) -> None:
        self.collection = collection or tasks_collection

    @staticmethod
    def _object_id(task_id: str) -> ObjectId | None:
        if not ObjectId.is_valid(task_id):
            return None
        return ObjectId(task_id)

    @staticmethod
    def _to_read(document: dict[str, Any]) -> MongoTaskRead:
        return MongoTaskRead(
            id=str(document["_id"]),
            title=document["title"],
            description=document["description"],
            importance=document["importance"],
            completed=document["completed"],
            created_at=document["created_at"],
            updated_at=document["updated_at"],
        )

    def list(self, *, offset: int, limit: int) -> list[MongoTaskRead]:
        cursor = (
            self.collection.find()
            .sort([("importance", -1), ("created_at", -1)])
            .skip(offset)
            .limit(limit)
        )
        return [self._to_read(document) for document in cursor]

    def get(self, task_id: str) -> MongoTaskRead | None:
        object_id = self._object_id(task_id)
        if object_id is None:
            return None
        document = self.collection.find_one({"_id": object_id})
        return self._to_read(document) if document else None

    def create(self, data: TaskCreate) -> MongoTaskRead:
        now = datetime.now(timezone.utc)
        document = {
            **data.model_dump(),
            "completed": False,
            "created_at": now,
            "updated_at": now,
        }
        result: InsertOneResult = self.collection.insert_one(document)
        document["_id"] = result.inserted_id
        return self._to_read(document)

    def update(self, task_id: str, data: TaskUpdate) -> MongoTaskRead | None:
        object_id = self._object_id(task_id)
        if object_id is None:
            return None

        updates = data.model_dump(exclude_unset=True)
        if updates:
            updates["updated_at"] = datetime.now(timezone.utc)
            self.collection.update_one({"_id": object_id}, {"$set": updates})

        document = self.collection.find_one({"_id": object_id})
        return self._to_read(document) if document else None

    def delete(self, task_id: str) -> bool:
        object_id = self._object_id(task_id)
        if object_id is None:
            return False
        result = self.collection.delete_one({"_id": object_id})
        return result.deleted_count == 1
