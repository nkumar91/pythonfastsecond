from fastapi import APIRouter
from app.api.endpoints import auth
from app.api.endpoints import product
from app.api.endpoints import category

main_router = APIRouter()

main_router.include_router(
    auth.users,
    prefix="/auth",
    tags=["auth"]
)

main_router.include_router(
    product.product_router,
    prefix="/products",
    tags=["products"]
)

main_router.include_router(
    category.category_router,
    prefix="/categories",
    tags=["categories"]
)