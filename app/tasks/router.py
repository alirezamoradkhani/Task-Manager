from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.tasks.schema import TaskCreate, TaskRead, TaskUpdate
from app.tasks.service import TaskNotFoundError, TaskService


router = APIRouter(prefix="/tasks", tags=["tasks"])
service = TaskService()
DatabaseSession = Annotated[Session, Depends(get_db)]


def not_found() -> HTTPException:
    return HTTPException(status_code=404, detail="Task not found")


@router.post("", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
def create_task(data: TaskCreate, db: DatabaseSession) -> TaskRead:
    return service.create(db, data)


@router.get("", response_model=list[TaskRead])
def list_tasks(
    db: DatabaseSession,
    offset: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 50,
) -> list[TaskRead]:
    return service.list(db, offset=offset, limit=limit)


@router.get("/{task_id}", response_model=TaskRead)
def get_task(task_id: int, db: DatabaseSession) -> TaskRead:
    try:
        return service.get(db, task_id)
    except TaskNotFoundError as error:
        raise not_found() from error


@router.patch("/{task_id}", response_model=TaskRead)
def update_task(task_id: int, data: TaskUpdate, db: DatabaseSession) -> TaskRead:
    try:
        return service.update(db, task_id, data)
    except TaskNotFoundError as error:
        raise not_found() from error


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int, db: DatabaseSession) -> Response:
    try:
        service.delete(db, task_id)
    except TaskNotFoundError as error:
        raise not_found() from error
    return Response(status_code=status.HTTP_204_NO_CONTENT)
