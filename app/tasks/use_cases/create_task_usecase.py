from app.tasks.repository import TaskRepository
from app.tasks.schema import TaskCreate, TaskRead


def create_task(repository: TaskRepository, data: TaskCreate) -> TaskRead:
    return repository.create(data)
