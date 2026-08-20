from sqlalchemy import select
from sqlalchemy.orm import Session

from app.tasks.model import Task
from app.tasks.schema import TaskCreate, TaskUpdate


class TaskRepository:
    def list(self, db: Session, *, offset: int, limit: int) -> list[Task]:
        statement = (
            select(Task)
            .order_by(Task.importance.desc(), Task.created_at.desc())
            .offset(offset)
            .limit(limit)
        )
        return list(db.scalars(statement))

    def get(self, db: Session, task_id: int) -> Task | None:
        return db.get(Task, task_id)

    def create(self, db: Session, data: TaskCreate) -> Task:
        task = Task(**data.model_dump())
        db.add(task)
        db.commit()
        db.refresh(task)
        return task

    def update(self, db: Session, task: Task, data: TaskUpdate) -> Task:
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(task, field, value)
        db.commit()
        db.refresh(task)
        return task

    def delete(self, db: Session, task: Task) -> None:
        db.delete(task)
        db.commit()
