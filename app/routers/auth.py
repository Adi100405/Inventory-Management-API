from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.auth.hashing import hash_password
from app.database.database import get_db
from app.schemas.user import UserCreate
from app.models.user import User
from app.schemas.auth import LoginRequest
from app.auth.hashing import verify_password
from app.auth.security import create_access_token

router = APIRouter()

@router.get("/health")
def health_check():
    return {
        "status": "healthy"
    }
    
@router.post("/register")
def register(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    existing_user = db.query(User).filter(
        User.email == user.email
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    hashed_password = hash_password(
        user.password
    )

    new_user = User(
        username=user.username,
        email=user.email,
        password=hashed_password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "id": new_user.id,
        "username": new_user.username,
        "email": new_user.email
    }

@router.post("/login")
def login(
    credentials: LoginRequest,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(
        User.email == credentials.email
    ).first()

    if not user:
        return {
            "message": "Invalid credentials"
        }

    if not verify_password(
        credentials.password,
        user.password
    ):
        return {
            "message": "Invalid credentials"
        }

    token = create_access_token(
        {
            "sub": user.email
        }
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }