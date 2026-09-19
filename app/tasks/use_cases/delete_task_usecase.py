from app.tasks.exceptions import TaskNotFoundError
from app.tasks.repository import TaskRepository


def delete_task(repository: TaskRepository, task_id: str) -> None:
    if not repository.delete(task_id):
        raise TaskNotFoundError
