from app.tasks.repository import TaskRepository
from app.tasks.schema import TaskRead


class ListTasksUseCase:
    def __init__(self, repository: TaskRepository) -> None:
        self.repository = repository

    def execute(self, *, offset: int, limit: int) -> list[TaskRead]:
        return self.repository.list(offset=offset, limit=limit)
