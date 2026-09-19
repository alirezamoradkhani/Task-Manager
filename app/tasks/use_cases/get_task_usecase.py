from app.tasks.exceptions import TaskNotFoundError
from app.tasks.repository import TaskRepository
from app.tasks.schema import TaskRead


def get_task(repository: TaskRepository, task_id: str) -> TaskRead:
    task = repository.get(task_id)
    if task is None:
        raise TaskNotFoundError
    return task
