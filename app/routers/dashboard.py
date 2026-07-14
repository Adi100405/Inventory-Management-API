from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database.database import get_db

from app.models.product import Product
from app.models.Category import Category
from app.models.transaction import InventoryTransaction

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)

@router.get("/stats")
def get_dashboard_stats(
    db: Session = Depends(get_db)
):
    total_products = db.query(Product).count()

    total_categories = db.query(Category).count()

    total_transactions = db.query(
        InventoryTransaction
    ).count()

    total_stock = db.query(
        func.sum(Product.quantity)
    ).scalar() or 0

    return {
        "total_products": total_products,
        "total_categories": total_categories,
        "total_transactions": total_transactions,
        "total_stock": total_stock
    }

@router.get("/recent-transactions")
def recent_transactions(
    db: Session = Depends(get_db)
):
    return db.query(
        InventoryTransaction
    ).order_by(
        InventoryTransaction.id.desc()
    ).limit(5).all()