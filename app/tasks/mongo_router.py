from typing import Annotated

from fastapi import APIRouter, HTTPException, Query, Response, status

from app.tasks.mongo_service import MongoTaskNotFoundError, MongoTaskService
from app.tasks.schema import MongoTaskRead, TaskCreate, TaskUpdate


router = APIRouter(prefix="/mongo/tasks", tags=["mongo-tasks"])
service = MongoTaskService()


def not_found() -> HTTPException:
    return HTTPException(status_code=404, detail="MongoDB task not found")


@router.post("", response_model=MongoTaskRead, status_code=status.HTTP_201_CREATED)
def create_task(data: TaskCreate) -> MongoTaskRead:
    return service.create(data)


@router.get("", response_model=list[MongoTaskRead])
def list_tasks(
    offset: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 50,
) -> list[MongoTaskRead]:
    return service.list(offset=offset, limit=limit)


@router.get("/{task_id}", response_model=MongoTaskRead)
def get_task(task_id: str) -> MongoTaskRead:
    try:
        return service.get(task_id)
    except MongoTaskNotFoundError as error:
        raise not_found() from error


@router.patch("/{task_id}", response_model=MongoTaskRead)
def update_task(task_id: str, data: TaskUpdate) -> MongoTaskRead:
    try:
        return service.update(task_id, data)
    except MongoTaskNotFoundError as error:
        raise not_found() from error


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: str) -> Response:
    try:
        service.delete(task_id)
    except MongoTaskNotFoundError as error:
        raise not_found() from error
    return Response(status_code=status.HTTP_204_NO_CONTENT)
