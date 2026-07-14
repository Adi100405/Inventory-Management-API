from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.auth.hashing import hash_password
from app.database.database import get_db
from app.schemas.user import UserCreate
from app.models.user import User

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