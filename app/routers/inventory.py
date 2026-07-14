from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db

from app.models.product import Product
from app.models.transaction import InventoryTransaction

from app.schemas.transaction import StockTransaction

router = APIRouter(
    prefix="/inventory",
    tags=["Inventory"]
)

@router.post("/stock-in")
def stock_in(
    transaction: StockTransaction,
    db: Session = Depends(get_db)
):
    product = db.query(Product).filter(
        Product.id == transaction.product_id
    ).first()

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    product.quantity += transaction.quantity

    log = InventoryTransaction(
        product_id=product.id,
        transaction_type="IN",
        quantity=transaction.quantity
    )

    db.add(log)

    db.commit()

    return {
        "message": "Stock added",
        "current_stock": product.quantity
    }

@router.post("/stock-out")
def stock_out(
    transaction: StockTransaction,
    db: Session = Depends(get_db)
):
    product = db.query(Product).filter(
        Product.id == transaction.product_id
    ).first()

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    if product.quantity < transaction.quantity:
        raise HTTPException(
            status_code=400,
            detail="Insufficient stock"
        )

    product.quantity -= transaction.quantity

    log = InventoryTransaction(
        product_id=product.id,
        transaction_type="OUT",
        quantity=transaction.quantity
    )

    db.add(log)

    db.commit()

    return {
        "message": "Stock removed",
        "current_stock": product.quantity
    }

@router.get("/transactions")
def get_transactions(
    db: Session = Depends(get_db)
):
    return db.query(
        InventoryTransaction
    ).all()