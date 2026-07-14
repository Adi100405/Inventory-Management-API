from pydantic import BaseModel

class StockTransaction(BaseModel):
    product_id: int
    quantity: int