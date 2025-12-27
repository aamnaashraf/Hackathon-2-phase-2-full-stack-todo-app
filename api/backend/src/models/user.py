from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime
import uuid
from pydantic import BaseModel, field_validator

class UserBase(SQLModel):
    email: str = Field(unique=True, index=True)

class User(UserBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    email: str = Field(unique=True, index=True)
    password_hash: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    is_active: bool = Field(default=True)

    # Relationship to todos
    todos: List["Todo"] = Relationship(back_populates="user")

class UserCreate(UserBase):
    password: str

    @field_validator("password")
    @classmethod
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters long")
        if len(v.encode('utf-8')) > 72:
            raise ValueError("Password must not exceed 72 bytes when encoded")
        return v

class UserRead(UserBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    is_active: bool

class UserUpdate(SQLModel):
    email: Optional[str] = None
    is_active: Optional[bool] = None

class UserLogin(SQLModel):
    email: str
    password: str

class UserPublic(UserBase):
    id: uuid.UUID
    created_at: datetime