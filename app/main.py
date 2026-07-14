from fastapi import FastAPI
from app.routers import Category
from app.models.user import User
from app.database.database import engine, Base
from app.routers import auth
from app.routers import product

Base.metadata.create_all(bind=engine)
app = FastAPI()

app.include_router(
    auth.router,
    prefix="/auth",
    tags=["Authentication"]
)
app.include_router(Category.router)

app.include_router(product.router)