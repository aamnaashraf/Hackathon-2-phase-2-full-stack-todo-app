import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel, create_engine, Session, select
from dotenv import load_dotenv
from typing import Generator

# Load environment variables
load_dotenv()

# Database setup - similar to backend/src/database/database.py
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    # For Vercel deployment, provide a fallback or raise an error
    DATABASE_URL = os.getenv("VERCEL_POSTGRES_URL", "sqlite:///./test.db")  # fallback for testing

engine = create_engine(DATABASE_URL, echo=True)

def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session

# Import models - similar to backend/src/models
from sqlmodel import Field, SQLModel
from datetime import datetime
from enum import Enum
from pydantic import BaseModel, EmailStr
from typing import Optional

class UserBase(SQLModel):
    email: EmailStr

class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True)
    hashed_password: str
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

class Todo(TodoBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

class TodoCreate(TodoBase):
    pass

class TodoUpdate(SQLModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None
    due_date: Optional[datetime] = None
    priority: Optional[Priority] = None

# Auth services - simplified version
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
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
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Create the FastAPI app
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create database tables on startup
    SQLModel.metadata.create_all(bind=engine)
    yield
    # Cleanup on shutdown if needed

app = FastAPI(
    title="Todo Web Application API",
    description="API for the Full-Stack Secure Todo Web Application",
    version="1.0.0",
    lifespan=lifespan
)

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
from fastapi import APIRouter, HTTPException, status

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
from typing import List

todo_router = APIRouter()

@todo_router.get("/api/todos", response_model=List[Todo])
def get_todos(session: Session = Depends(get_session)):
    """
    Get all todos for the authenticated user
    """
    # For simplicity, returning all todos - in real app, filter by user_id
    todos = session.exec(select(Todo)).all()
    return todos

@todo_router.post("/api/todos", response_model=Todo)
def create_todo(todo_create: TodoCreate, session: Session = Depends(get_session)):
    """
    Create a new todo
    """
    # For simplicity, creating without user context - in real app, get user from token
    db_todo = Todo(
        title=todo_create.title,
        description=todo_create.description,
        due_date=todo_create.due_date,
        priority=todo_create.priority
    )
    session.add(db_todo)
    session.commit()
    session.refresh(db_todo)
    return db_todo

@todo_router.get("/api/todos/{todo_id}", response_model=Todo)
def get_todo(todo_id: int, session: Session = Depends(get_session)):
    """
    Get a specific todo by ID
    """
    todo = session.get(Todo, todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo

@todo_router.put("/api/todos/{todo_id}", response_model=Todo)
def update_todo(todo_id: int, todo_update: TodoUpdate, session: Session = Depends(get_session)):
    """
    Update a specific todo by ID
    """
    todo = session.get(Todo, todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")

    # Update the todo with provided values
    for field, value in todo_update.dict(exclude_unset=True).items():
        setattr(todo, field, value)

    session.add(todo)
    session.commit()
    session.refresh(todo)
    return todo

@todo_router.delete("/api/todos/{todo_id}")
def delete_todo(todo_id: int, session: Session = Depends(get_session)):
    """
    Delete a specific todo by ID
    """
    todo = session.get(Todo, todo_id)
    if not todo:
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