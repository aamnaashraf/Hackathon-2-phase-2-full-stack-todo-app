from sqlmodel import Session, select
from typing import List, Optional
from uuid import UUID
from ..models.todo import Todo, TodoCreate, TodoUpdate
from ..models.user import User
from fastapi import HTTPException, status

def create_todo(session: Session, todo_create: TodoCreate, user_id: str) -> Todo:
    """
    Create a new todo for a user
    """
    todo = Todo(
        **todo_create.model_dump(),
        user_id=UUID(user_id)
    )

    session.add(todo)
    session.commit()
    session.refresh(todo)

    return todo

def get_todos(session: Session, user_id: str) -> List[Todo]:
    """
    Get all todos for a specific user
    """
    statement = select(Todo).where(Todo.user_id == UUID(user_id))
    todos = session.exec(statement).all()
    return todos

def get_todo(session: Session, todo_id: str, user_id: str) -> Todo:
    """
    Get a specific todo by ID for a specific user
    """
    statement = select(Todo).where(Todo.id == UUID(todo_id), Todo.user_id == UUID(user_id))
    todo = session.exec(statement).first()

    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )

    return todo

def update_todo(session: Session, todo_id: str, todo_update: TodoUpdate, user_id: str) -> Todo:
    """
    Update a specific todo by ID for a specific user
    """
    todo = get_todo(session, todo_id, user_id)

    # Update the todo with provided values
    update_data = todo_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(todo, field, value)

    session.add(todo)
    session.commit()
    session.refresh(todo)

    return todo

def delete_todo(session: Session, todo_id: str, user_id: str) -> bool:
    """
    Delete a specific todo by ID for a specific user
    """
    todo = get_todo(session, todo_id, user_id)

    session.delete(todo)
    session.commit()

    return True