from app.tasks.repository import TaskRepository
from app.tasks.schema import TaskCreate, TaskRead


class CreateTaskUseCase:
    def __init__(self, repository: TaskRepository) -> None:
        self.repository = repository

    def execute(self, data: TaskCreate) -> TaskRead:
        return self.repository.create(data)
