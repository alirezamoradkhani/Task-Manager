from datetime import datetime

from pydantic import BaseModel, Field, field_validator


class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    description: str = ""
    importance: int = Field(default=0, ge=0, le=5)


class TaskUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=200)
    description: str | None = None
    importance: int | None = Field(default=None, ge=0, le=5)
    completed: bool | None = None

    @field_validator("title", "description", "importance", "completed")
    @classmethod
    def reject_explicit_null(cls, value: str | int | bool | None) -> str | int | bool:
        if value is None:
            raise ValueError("Omit the field to leave it unchanged; null is not allowed")
        return value


class TaskRead(BaseModel):
    """Public representation of a task stored in MongoDB."""

    id: str
    title: str
    description: str
    importance: int
    completed: bool
    created_at: datetime
    updated_at: datetime
