from app.tasks.exceptions import TaskNotFoundError
from app.tasks.repository import TaskRepository
from app.tasks.schema import TaskRead


class GetTaskUseCase:
    def __init__(self, repository: TaskRepository) -> None:
        self.repository = repository

    def execute(self, task_id: str) -> TaskRead:
        task = self.repository.get(task_id)
        if task is None:
            raise TaskNotFoundError
        return task
