from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.Category import Category
from app.schemas.Category import CategoryCreate

router = APIRouter(
    prefix="/categories",
    tags=["Categories"]
)

@router.post("/")
def create_category(
    category: CategoryCreate,
    db: Session = Depends(get_db)
):
    new_category = Category(
        name=category.name
    )

    db.add(new_category)
    db.commit()
    db.refresh(new_category)

    return new_category

@router.get("/")
def get_categories(
    db: Session = Depends(get_db)
):
    return db.query(Category).all()

@router.put("/{category_id}")
def update_category(
    category_id: int,
    category: CategoryCreate,
    db: Session = Depends(get_db)
):
    existing_category = db.query(
        Category
    ).filter(
        Category.id == category_id
    ).first()

    if not existing_category:
        return {
            "message": "Category not found"
        }

    existing_category.name = category.name

    db.commit()
    db.refresh(existing_category)

    return existing_category

@router.delete("/{category_id}")
def delete_category(
    category_id: int,
    db: Session = Depends(get_db)
):
    category = db.query(
        Category
    ).filter(
        Category.id == category_id
    ).first()

    if not category:
        return {
            "message": "Category not found"
        }

    db.delete(category)

    db.commit()

    return {
        "message": "Category deleted successfully"
    }