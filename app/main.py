"""Точка входа."""

from fastapi import FastAPI

from app.presentation.api.exception_handlers import register_exception_handlers
from app.presentation.api.router import api_router

app = FastAPI()

app.include_router(
    api_router,
    prefix="/api/v1",
)

register_exception_handlers(app)
