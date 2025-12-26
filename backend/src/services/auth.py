from datetime import datetime, timedelta
from typing import Optional
from sqlmodel import Session, select
from passlib.context import CryptContext
import bcrypt
from jose import JWTError, jwt
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from uuid import UUID
from ..models.user import User, UserCreate
from ..database.database import get_session
import os
from dotenv import load_dotenv

load_dotenv()

# Using bcrypt directly to avoid initialization issues with long passwords

# JWT settings
SECRET_KEY = os.getenv("SECRET_KEY", "your-super-secret-key-change-in-production")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

# Security scheme for API docs
security = HTTPBearer()

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain password against a hashed password.
    Truncate the password if it exceeds 72 bytes to avoid bcrypt errors.
    """
    # Truncate the password if it exceeds 71 bytes to avoid bcrypt errors
    if len(plain_password.encode('utf-8')) > 71:
        # Truncate the password string to ensure it fits within 71 bytes
        truncated_password = plain_password
        while len(truncated_password.encode('utf-8')) > 71:
            truncated_password = truncated_password[:-1]
        plain_password = truncated_password

    # Encode both passwords to bytes for comparison
    password_bytes = plain_password.encode('utf-8')
    hashed_bytes = hashed_password.encode('utf-8')
    return bcrypt.checkpw(password_bytes, hashed_bytes)

def get_password_hash(password: str) -> str:
    """
    Hash a password with bcrypt, ensuring it's within the 72-byte limit.
    Bcrypt has a hard limit of 72 bytes, so we truncate if necessary.
    We truncate at character boundaries to avoid splitting multi-byte characters.
    """
    # Validate password length before hashing
    if len(password) < 8:
        raise ValueError("Password must be at least 8 characters long")

    # Ensure the password is within bcrypt's 72-byte limit
    # We truncate to 71 bytes to have a safety margin
    if len(password.encode('utf-8')) > 71:
        # Truncate the password string to ensure it fits within 71 bytes
        # We'll iteratively reduce the string length until it fits
        truncated_password = password
        while len(truncated_password.encode('utf-8')) > 71:
            truncated_password = truncated_password[:-1]
        password = truncated_password

    # Encode password to bytes and hash it with bcrypt
    password_bytes = password.encode('utf-8')
    hashed_bytes = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
    return hashed_bytes.decode('utf-8')

def authenticate_user(session: Session, email: str, password: str) -> Optional[User]:
    """
    Authenticate a user by email and password
    """
    statement = select(User).where(User.email == email)
    user = session.exec(statement).first()

    if not user or not verify_password(password, user.password_hash):
        return None

    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    Create a JWT access token
    """
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    session: Session = Depends(get_session)
) -> User:
    """
    Get the current user from the JWT token
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")

        if email is None:
            raise credentials_exception

        token_data = TokenData(username=email)
    except JWTError:
        raise credentials_exception

    statement = select(User).where(User.email == token_data.username)
    user = session.exec(statement).first()

    if user is None:
        raise credentials_exception

    return user

def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    """
    Get the current active user
    """
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

def create_user(session: Session, user_create: UserCreate) -> User:
    """
    Create a new user with hashed password
    """
    # Hash the password
    hashed_password = get_password_hash(user_create.password)

    # Create the user object
    user = User(
        email=user_create.email,
        password_hash=hashed_password
    )

    # Add to session and commit
    session.add(user)
    session.commit()
    session.refresh(user)

    return user