from app.tasks.repository import TaskRepository
from app.tasks.schema import TaskRead, TaskCreate, TaskUpdate


class TaskNotFoundError(Exception):
    pass


class TaskService:
    def __init__(self, repository: TaskRepository | None = None) -> None:
        self.repository = repository or TaskRepository()

    def list(self, *, offset: int, limit: int) -> list[TaskRead]:
        return self.repository.list(offset=offset, limit=limit)

    def get(self, task_id: str) -> TaskRead:
        task = self.repository.get(task_id)
        if task is None:
            raise TaskNotFoundError
        return task

    def create(self, data: TaskCreate) -> TaskRead:
        return self.repository.create(data)

    def update(self, task_id: str, data: TaskUpdate) -> TaskRead:
        task = self.repository.update(task_id, data)
        if task is None:
            raise TaskNotFoundError
        return task

    def delete(self, task_id: str) -> None:
        if not self.repository.delete(task_id):
            raise TaskNotFoundError
