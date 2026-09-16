from typing import Annotated

from fastapi import APIRouter, HTTPException, Query, Response, status

from app.tasks.service import TaskNotFoundError, TaskService
from app.tasks.schema import TaskRead, TaskCreate, TaskUpdate


router = APIRouter(prefix="/tasks", tags=["tasks"])
service = TaskService()


def not_found() -> HTTPException:
    return HTTPException(status_code=404, detail="Task not found")


@router.post("", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
def create_task(data: TaskCreate) -> TaskRead:
    return service.create(data)


@router.get("", response_model=list[TaskRead])
def list_tasks(
    offset: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 50,
) -> list[TaskRead]:
    return service.list(offset=offset, limit=limit)


@router.get("/{task_id}", response_model=TaskRead)
def get_task(task_id: str) -> TaskRead:
    try:
        return service.get(task_id)
    except TaskNotFoundError as error:
        raise not_found() from error


@router.patch("/{task_id}", response_model=TaskRead)
def update_task(task_id: str, data: TaskUpdate) -> TaskRead:
    try:
        return service.update(task_id, data)
    except TaskNotFoundError as error:
        raise not_found() from error


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: str) -> Response:
    try:
        service.delete(task_id)
    except TaskNotFoundError as error:
        raise not_found() from error
    return Response(status_code=status.HTTP_204_NO_CONTENT)
