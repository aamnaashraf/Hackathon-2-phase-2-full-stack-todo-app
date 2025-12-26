from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from datetime import timedelta
from ..database.database import get_session
from ..models.user import User, UserCreate, UserLogin, UserPublic
from ..services.auth import (
    authenticate_user,
    create_access_token,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    create_user
)

router = APIRouter()

@router.post("/register", response_model=UserPublic)
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

@router.post("/login")
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

@router.post("/logout")
def logout():
    """
    Logout a user (currently just a placeholder)
    """
    return {"message": "Successfully logged out"}