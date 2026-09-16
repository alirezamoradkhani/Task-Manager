from app.tasks.exceptions import TaskNotFoundError
from app.tasks.repository import TaskRepository
from app.tasks.schema import TaskRead, TaskUpdate


class UpdateTaskUseCase:
    def __init__(self, repository: TaskRepository) -> None:
        self.repository = repository

    def execute(self, task_id: str, data: TaskUpdate) -> TaskRead:
        task = self.repository.update(task_id, data)
        if task is None:
            raise TaskNotFoundError
        return task
