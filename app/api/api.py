from fastapi import APIRouter
from app.api.endpoints import auth

main_router = APIRouter()

main_router.include_router(
    auth.users,
    prefix="/auth",
    tags=["auth"]
)