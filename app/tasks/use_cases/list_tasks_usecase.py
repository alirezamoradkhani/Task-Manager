from app.tasks.repository import TaskRepository
from app.tasks.schema import TaskRead


def list_tasks(repository: TaskRepository, *, offset: int, limit: int) -> list[TaskRead]:
    return repository.list(offset=offset, limit=limit)
