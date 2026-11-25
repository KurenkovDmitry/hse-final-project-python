"""Роутер."""

from fastapi import APIRouter, Depends

from app.presentation.api.routers.auth import get_current_session
from app.presentation.api.routers.auth import router as auth_router
from app.presentation.api.routers.users import router as users_router
from app.presentation.api.routers.students import router as students_router

api_router = APIRouter()
api_router.include_router(auth_router, prefix="/auth", tags=["auth"])

api_router.include_router(
    users_router,
    prefix="/users",
    tags=["users"],
    dependencies=[Depends(get_current_session)],
)

api_router.include_router(
    students_router,
    prefix="/students",
    tags=["students"],
    dependencies=[Depends(get_current_session)],
)
