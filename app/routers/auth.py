from fastapi import APIRouter , Depends
from sqlalchemy.orm import Session
from app.auth.hashing import hash_password
from app.database.database import get_db
from app.schemas.user import UserCreate

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
    hashed_password = hash_password(user.password)

    return {
        "username": user.username,
        "hashed_password": hashed_password
    }