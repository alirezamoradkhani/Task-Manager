from sqlalchemy.orm import Session

from app.tasks.model import Task
from app.tasks.repository import TaskRepository
from app.tasks.schema import TaskCreate, TaskUpdate


class TaskNotFoundError(Exception):
    pass


class TaskService:
    def __init__(self, repository: TaskRepository | None = None) -> None:
        self.repository = repository or TaskRepository()

    def list(self, db: Session, *, offset: int, limit: int) -> list[Task]:
        return self.repository.list(db, offset=offset, limit=limit)

    def get(self, db: Session, task_id: int) -> Task:
        task = self.repository.get(db, task_id)
        if task is None:
            raise TaskNotFoundError
        return task

    def create(self, db: Session, data: TaskCreate) -> Task:
        return self.repository.create(db, data)

    def update(self, db: Session, task_id: int, data: TaskUpdate) -> Task:
        task = self.get(db, task_id)
        return self.repository.update(db, task, data)

    def delete(self, db: Session, task_id: int) -> None:
        task = self.get(db, task_id)
        self.repository.delete(db, task)
