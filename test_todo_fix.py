#!/usr/bin/env python3
"""
Test script to verify the todo creation fix works correctly
"""
import sys
import os
import uuid
from datetime import datetime

# Add the backend directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend/src'))

from backend.src.models.todo import TodoCreate, TodoUpdate
from backend.src.services.todo_service import create_todo
from sqlmodel import Session, create_engine
from backend.src.database.database import DATABASE_URL

def test_todo_creation():
    print("Testing todo creation model validation...")

    # Test valid todo creation
    try:
        todo_create = TodoCreate(title="Test Todo", description="Test Description", due_date="2024-12-31")
        print(f"[PASS] Valid todo creation: {todo_create.title}")
        print(f"  Due date: {todo_create.due_date}")
    except Exception as e:
        print(f"[FAIL] Error with valid todo: {e}")

    # Test minimal todo (title only)
    try:
        todo_create = TodoCreate(title="Simple Todo")
        print(f"[PASS] Minimal todo creation: {todo_create.title}")
    except Exception as e:
        print(f"[FAIL] Error with minimal todo: {e}")

    # Test empty title (should fail)
    try:
        todo_create = TodoCreate(title="")
        print(f"[FAIL] Empty title should have failed: {todo_create.title}")
    except Exception as e:
        print(f"[PASS] Correctly rejected empty title: {type(e).__name__}")

    # Test date parsing
    try:
        todo_create = TodoCreate(title="Date Test", due_date="2024-12-31")
        print(f"[PASS] Date parsing: {todo_create.due_date}")
    except Exception as e:
        print(f"[FAIL] Error with date parsing: {e}")

    # Test update model validation
    try:
        todo_update = TodoUpdate(title="Updated Title", due_date="2024-12-31")
        print(f"[PASS] Valid todo update: {todo_update.title}")
        print(f"  Updated due date: {todo_update.due_date}")
    except Exception as e:
        print(f"[FAIL] Error with todo update: {e}")

if __name__ == "__main__":
    test_todo_creation()