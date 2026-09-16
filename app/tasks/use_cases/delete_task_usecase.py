from app.tasks.exceptions import TaskNotFoundError
from app.tasks.repository import TaskRepository


class DeleteTaskUseCase:
    def __init__(self, repository: TaskRepository) -> None:
        self.repository = repository

    def execute(self, task_id: str) -> None:
        if not self.repository.delete(task_id):
            raise TaskNotFoundError
