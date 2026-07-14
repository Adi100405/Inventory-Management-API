from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.product import Product
from app.schemas.product import ProductCreate

router = APIRouter(
    prefix="/products",
    tags=["Products"]
)

@router.post("/")
def create_product(
    product: ProductCreate,
    db: Session = Depends(get_db)
):
    new_product = Product(
        name=product.name,
        price=product.price,
        quantity=product.quantity,
        category_id=product.category_id
    )

    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return new_product

@router.get("/")
def get_products(
    db: Session = Depends(get_db)
):
    return db.query(Product).all()