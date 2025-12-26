from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from datetime import datetime
import uuid
from pydantic import field_validator, model_validator
from .user import User
from enum import Enum


class PriorityEnum(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"


class TodoBase(SQLModel):
    title: str
    description: Optional[str] = None
    completed: bool = False
    due_date: Optional[datetime] = None
    priority: Optional[PriorityEnum] = PriorityEnum.medium

    @model_validator(mode="before")
    @classmethod
    def validate_title_not_empty(cls, values):
        if isinstance(values, dict) and values.get("title") == "":
            raise ValueError("Title cannot be empty")
        return values

    @field_validator("due_date", mode="before")
    @classmethod
    def validate_due_date(cls, v):
        if isinstance(v, str):
            try:
                # Try to parse the date string (ISO format from frontend)
                return datetime.fromisoformat(v.replace('Z', '+00:00'))
            except ValueError:
                # If ISO format fails, try other formats
                try:
                    return datetime.strptime(v, "%Y-%m-%d")
                except ValueError:
                    raise ValueError("Invalid date format. Use ISO format (YYYY-MM-DD) or YYYY-MM-DD")
        return v


class Todo(TodoBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    title: str
    description: Optional[str] = None
    completed: bool = False
    # FIXED LINE: ondelete hata diya
    user_id: uuid.UUID = Field(foreign_key="user.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    due_date: Optional[datetime] = None

    # Relationship to user
    user: "User" = Relationship(back_populates="todos")


class TodoCreate(TodoBase):
    pass


class TodoRead(TodoBase):
    id: uuid.UUID
    user_id: uuid.UUID
    created_at: datetime
    updated_at: datetime


class TodoUpdate(SQLModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None
    due_date: Optional[datetime] = None
    priority: Optional[PriorityEnum] = None

    @field_validator("due_date", mode="before")
    @classmethod
    def validate_due_date(cls, v):
        if isinstance(v, str):
            try:
                # Try to parse the date string (ISO format from frontend)
                return datetime.fromisoformat(v.replace('Z', '+00:00'))
            except ValueError:
                # If ISO format fails, try other formats
                try:
                    return datetime.strptime(v, "%Y-%m-%d")
                except ValueError:
                    raise ValueError("Invalid date format. Use ISO format (YYYY-MM-DD) or YYYY-MM-DD")
        return v


class TodoPublic(TodoBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime