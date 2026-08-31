from app.tasks.mongo_repository import MongoTaskRepository
from app.tasks.schema import MongoTaskRead, TaskCreate, TaskUpdate


class MongoTaskNotFoundError(Exception):
    pass


class MongoTaskService:
    def __init__(self, repository: MongoTaskRepository | None = None) -> None:
        self.repository = repository or MongoTaskRepository()

    def list(self, *, offset: int, limit: int) -> list[MongoTaskRead]:
        return self.repository.list(offset=offset, limit=limit)

    def get(self, task_id: str) -> MongoTaskRead:
        task = self.repository.get(task_id)
        if task is None:
            raise MongoTaskNotFoundError
        return task

    def create(self, data: TaskCreate) -> MongoTaskRead:
        return self.repository.create(data)

    def update(self, task_id: str, data: TaskUpdate) -> MongoTaskRead:
        task = self.repository.update(task_id, data)
        if task is None:
            raise MongoTaskNotFoundError
        return task

    def delete(self, task_id: str) -> None:
        if not self.repository.delete(task_id):
            raise MongoTaskNotFoundError
