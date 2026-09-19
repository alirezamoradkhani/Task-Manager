from app.tasks.exceptions import TaskNotFoundError
from app.tasks.repository import TaskRepository
from app.tasks.schema import TaskRead, TaskUpdate


def update_task(repository: TaskRepository, task_id: str, data: TaskUpdate) -> TaskRead:
    task = repository.update(task_id, data)
    if task is None:
        raise TaskNotFoundError
    return task
