from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, Response, status

from app.tasks.exceptions import TaskNotFoundError
from app.tasks.repository import TaskRepository
from app.tasks.schema import TaskCreate, TaskRead, TaskUpdate
from app.tasks.use_cases import (
    create_task as create_task_usecase,
    delete_task as delete_task_usecase,
    get_task as get_task_usecase,
    list_tasks as list_tasks_usecase,
    update_task as update_task_usecase,
)


router = APIRouter(prefix="/tasks", tags=["tasks"])


def get_task_repository() -> TaskRepository:
    return TaskRepository()


RepositoryDependency = Annotated[TaskRepository, Depends(get_task_repository)]


def not_found() -> HTTPException:
    return HTTPException(status_code=404, detail="Task not found")


@router.post("", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
def create_task(data: TaskCreate, repository: RepositoryDependency) -> TaskRead:
    return create_task_usecase(repository, data)


@router.get("", response_model=list[TaskRead])
def list_tasks(
    repository: RepositoryDependency,
    offset: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 50,
) -> list[TaskRead]:
    return list_tasks_usecase(repository, offset=offset, limit=limit)


@router.get("/{task_id}", response_model=TaskRead)
def get_task(task_id: str, repository: RepositoryDependency) -> TaskRead:
    try:
        return get_task_usecase(repository, task_id)
    except TaskNotFoundError as error:
        raise not_found() from error


@router.patch("/{task_id}", response_model=TaskRead)
def update_task(task_id: str, data: TaskUpdate, repository: RepositoryDependency) -> TaskRead:
    try:
        return update_task_usecase(repository, task_id, data)
    except TaskNotFoundError as error:
        raise not_found() from error


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: str, repository: RepositoryDependency) -> Response:
    try:
        delete_task_usecase(repository, task_id)
    except TaskNotFoundError as error:
        raise not_found() from error
    return Response(status_code=status.HTTP_204_NO_CONTENT)
