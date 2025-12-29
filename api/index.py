import os
from contextlib import contextmanager
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel, create_engine, Session, select
from dotenv import load_dotenv
from typing import Generator
from sqlalchemy.pool import NullPool
from sqlalchemy import create_engine as create_sqlalchemy_engine
from datetime import datetime, timedelta
import jwt
from jwt import PyJWTError
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials


# Load environment variables
load_dotenv()

# Database setup
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    # For Vercel deployment, provide a fallback or raise an error
    DATABASE_URL = os.getenv("VERCEL_POSTGRES_URL")
    if not DATABASE_URL:
        # For local development, you might want to use a local database
        # but in serverless context, DATABASE_URL must be provided
        raise ValueError("DATABASE_URL or VERCEL_POSTGRES_URL not found in environment variables")

# Create engine with NullPool for serverless compatibility
engine = create_sqlalchemy_engine(
    DATABASE_URL,
    poolclass=NullPool,
    pool_pre_ping=True,  # Verify connections before use
    pool_recycle=300,    # Recycle connections after 5 minutes
    echo=False           # Set to True for debugging
)


def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session


# Models
from sqlmodel import Field
from datetime import datetime
from enum import Enum
from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional


class UserBase(SQLModel):
    email: EmailStr


class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, nullable=False, sa_column_kwargs={"autoincrement": True})
    email: str = Field(unique=True, index=True)
    hashed_password: str = Field(sa_column_kwargs={"name": "password_hash"})  # Map to existing "password_hash" column
    created_at: datetime = Field(default_factory=datetime.now)


class UserCreate(UserBase):
    password: str


class UserLogin(UserBase):
    password: str


class UserPublic(UserBase):
    id: int
    created_at: datetime


class Priority(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"


class TodoBase(SQLModel):
    title: str
    description: Optional[str] = None
    completed: bool = False
    due_date: Optional[datetime] = None
    priority: Priority = Priority.medium

    @field_validator("due_date", mode="before", check_fields=False)
    @classmethod
    def validate_due_date(cls, v):
        if isinstance(v, str):
            try:
                # Try to parse the date string (ISO format from frontend)
                return datetime.fromisoformat(v.replace('Z', '+00:00').replace('T', ' '))
            except ValueError:
                # If ISO format fails, try other formats
                try:
                    return datetime.strptime(v, "%Y-%m-%d")
                except ValueError:
                    try:
                        return datetime.strptime(v, "%Y-%m-%d %H:%M:%S")
                    except ValueError:
                        raise ValueError("Invalid date format. Use ISO format (YYYY-MM-DDTHH:MM:SS) or YYYY-MM-DD")
        return v


class Todo(TodoBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, nullable=False, sa_column_kwargs={"autoincrement": True})
    user_id: int = Field(foreign_key="user.id", nullable=False)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


class TodoCreate(TodoBase):
    # Inherit all validation from TodoBase
    pass


class TodoUpdate(SQLModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None
    due_date: Optional[datetime] = None
    priority: Optional[Priority] = None

    @field_validator("due_date", mode="before", check_fields=False)
    @classmethod
    def validate_due_date(cls, v):
        if isinstance(v, str):
            try:
                # Try to parse the date string (ISO format from frontend)
                return datetime.fromisoformat(v.replace('Z', '+00:00').replace('T', ' '))
            except ValueError:
                # If ISO format fails, try other formats
                try:
                    return datetime.strptime(v, "%Y-%m-%d")
                except ValueError:
                    try:
                        return datetime.strptime(v, "%Y-%m-%d %H:%M:%S")
                    except ValueError:
                        raise ValueError("Invalid date format. Use ISO format (YYYY-MM-DDTHH:MM:SS) or YYYY-MM-DD")
        return v


# Auth services
from passlib.context import CryptContext
import bcrypt

SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Configure bcrypt to avoid version detection issues
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
    bcrypt__ident="2b",
    bcrypt__min_rounds=12
)
security = HTTPBearer()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def create_user(session: Session, user_create: UserCreate) -> User:
    hashed_password = get_password_hash(user_create.password)
    db_user = User(email=user_create.email, hashed_password=hashed_password)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


def authenticate_user(session: Session, email: str, password: str) -> Optional[User]:
    statement = select(User).where(User.email == email)
    user = session.exec(statement).first()
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_current_user(token: HTTPAuthorizationCredentials = Depends(security), session: Session = Depends(get_session)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except PyJWTError:
        raise credentials_exception
    statement = select(User).where(User.email == email)
    user = session.exec(statement).first()
    if user is None:
        raise credentials_exception
    return user


# Create database tables
def create_db_and_tables():
    try:
        # Create all tables defined in SQLModel metadata
        SQLModel.metadata.create_all(engine)
    except Exception as e:
        print(f"Error creating database tables: {e}")
        # In serverless environments, we might need to handle this differently
        # For now, we'll just log the error

# Create the FastAPI app
app = FastAPI()

@app.on_event("startup")
def on_startup():
    # In serverless environments, database tables should be pre-created
    # This is just a safety measure for local development
    try:
        create_db_and_tables()
    except Exception as e:
        print(f"Warning: Could not create database tables: {e}")
        print("Make sure your database schema is properly set up.")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    # Expose the authorization header to allow frontend to access JWT
    expose_headers=["Access-Control-Allow-Origin"]
)

# Auth router
from fastapi import APIRouter
from typing import List


auth_router = APIRouter()


@auth_router.post("/api/auth/register", response_model=UserPublic)
def register(user_create: UserCreate, session: Session = Depends(get_session)):
    """
    Register a new user
    """
    # Check if user already exists
    existing_user_statement = select(User).where(User.email == user_create.email)
    existing_user = session.exec(existing_user_statement).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this email already exists"
        )

    # Create the new user with error handling for debugging
    try:
        user = create_user(session, user_create)
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Registration failed: {str(e)}"
        )

    # Return public user data (without password hash)
    return UserPublic(
        id=user.id,
        email=user.email,
        created_at=user.created_at
    )


@auth_router.post("/api/auth/login")
def login(user_credentials: UserLogin, session: Session = Depends(get_session)):
    """
    Login a user and return access token
    """
    user = authenticate_user(
        session=session,
        email=user_credentials.email,
        password=user_credentials.password
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email},
        expires_delta=access_token_expires
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "email": user.email
        }
    }


@auth_router.post("/api/auth/logout")
def logout():
    """
    Logout a user (currently just a placeholder)
    """
    return {"message": "Successfully logged out"}


# Todo router
todo_router = APIRouter()


@todo_router.get("/api/todos", response_model=List[Todo])
def get_todos(current_user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    """
    Get all todos for the authenticated user
    """
    statement = select(Todo).where(Todo.user_id == current_user.id)
    todos = session.exec(statement).all()
    return todos


@todo_router.post("/api/todos", response_model=Todo)
def create_todo(todo_create: TodoCreate, current_user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    """
    Create a new todo for the authenticated user
    """
    # Explicitly handle all fields to ensure they are properly set
    db_todo = Todo(
        title=todo_create.title,
        description=todo_create.description if todo_create.description is not None else None,
        completed=todo_create.completed if hasattr(todo_create, 'completed') else False,
        due_date=todo_create.due_date if todo_create.due_date is not None else None,
        priority=todo_create.priority if todo_create.priority is not None else Priority.medium,
        user_id=current_user.id
    )
    session.add(db_todo)
    session.commit()
    session.refresh(db_todo)
    return db_todo


@todo_router.get("/api/todos/{todo_id}", response_model=Todo)
def get_todo(todo_id: int, current_user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    """
    Get a specific todo by ID for the authenticated user
    """
    todo = session.get(Todo, todo_id)
    if not todo or todo.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo


@todo_router.put("/api/todos/{todo_id}", response_model=Todo)
def update_todo(todo_id: int, todo_update: TodoUpdate, current_user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    """
    Update a specific todo by ID for the authenticated user
    """
    todo = session.get(Todo, todo_id)
    if not todo or todo.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Todo not found")

    # Update the todo with provided values
    for field, value in todo_update.dict(exclude_unset=True).items():
        setattr(todo, field, value)

    session.add(todo)
    session.commit()
    session.refresh(todo)
    return todo


@todo_router.delete("/api/todos/{todo_id}")
def delete_todo(todo_id: int, current_user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    """
    Delete a specific todo by ID for the authenticated user
    """
    todo = session.get(Todo, todo_id)
    if not todo or todo.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Todo not found")

    session.delete(todo)
    session.commit()
    return {"message": "Todo deleted successfully"}


# Include API routers
app.include_router(auth_router)
app.include_router(todo_router)


@app.get("/")
def read_root():
    return {"message": "Todo Web Application API - Deployed on Vercel"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}
