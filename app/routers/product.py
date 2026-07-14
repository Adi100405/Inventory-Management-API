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

@router.put("/{product_id}")
def update_product(
    product_id: int,
    product: ProductCreate,
    db: Session = Depends(get_db)
):
    existing_product = db.query(
        Product
    ).filter(
        Product.id == product_id
    ).first()

    if not existing_product:
        return {
            "message": "Product not found"
        }

    existing_product.name = product.name
    existing_product.price = product.price
    existing_product.quantity = product.quantity
    existing_product.category_id = product.category_id

    db.commit()

    db.refresh(existing_product)

    return existing_product

@router.delete("/{product_id}")
def delete_product(
    product_id: int,
    db: Session = Depends(get_db)
):
    product = db.query(
        Product
    ).filter(
        Product.id == product_id
    ).first()

    if not product:
        return {
            "message": "Product not found"
        }

    db.delete(product)

    db.commit()

    return {
        "message": "Product deleted successfully"
    }

