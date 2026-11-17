"""Роутер."""

from fastapi import APIRouter

from app.presentation.api.routers.users import router as users_router
from app.presentation.api.routers.students import router as students_router

api_router = APIRouter()

api_router.include_router(
    users_router,
    prefix="/users",
    tags=["users"],
)

api_router.include_router(
    students_router,
    prefix="/students",
    tags=["students"],
)
