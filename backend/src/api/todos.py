from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import List
from uuid import UUID
from ..database.database import get_session
from ..models.todo import Todo, TodoCreate, TodoRead, TodoUpdate, TodoPublic
from ..models.user import User
from ..services.todo_service import (
    create_todo,
    get_todos,
    get_todo,
    update_todo,
    delete_todo
)
from ..services.auth import get_current_active_user

router = APIRouter()

@router.get("/", response_model=List[TodoRead])
def read_todos(
    current_user: User = Depends(get_current_active_user),
    session: Session = Depends(get_session)
):
    """
    Get all todos for the current user
    """
    todos = get_todos(session, str(current_user.id))
    return todos

@router.post("/", response_model=TodoRead)
def create_todo_item(
    todo_create: TodoCreate,
    current_user: User = Depends(get_current_active_user),
    session: Session = Depends(get_session)
):
    """
    Create a new todo for the current user
    """
    try:
        todo = create_todo(session, todo_create, str(current_user.id))
        return todo
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Failed to create todo: {str(e)}"
        )

@router.get("/{todo_id}", response_model=TodoRead)
def read_todo(
    todo_id: UUID,
    current_user: User = Depends(get_current_active_user),
    session: Session = Depends(get_session)
):
    """
    Get a specific todo by ID
    """
    todo = get_todo(session, str(todo_id), str(current_user.id))
    return todo

@router.put("/{todo_id}", response_model=TodoRead)
def update_todo_item(
    todo_id: UUID,
    todo_update: TodoUpdate,
    current_user: User = Depends(get_current_active_user),
    session: Session = Depends(get_session)
):
    """
    Update a specific todo by ID
    """
    todo = update_todo(session, str(todo_id), todo_update, str(current_user.id))
    return todo

@router.delete("/{todo_id}")
def delete_todo_item(
    todo_id: UUID,
    current_user: User = Depends(get_current_active_user),
    session: Session = Depends(get_session)
):
    """
    Delete a specific todo by ID
    """
    delete_todo(session, str(todo_id), str(current_user.id))
    return {"message": "Todo deleted successfully"}