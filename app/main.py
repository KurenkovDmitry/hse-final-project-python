"""Точка входа."""

import os
import secrets

from fastapi import FastAPI

from _collections_abc import AsyncIterator
from contextlib import asynccontextmanager

from app.container import engine
from app.domain.entities.student import Base
from app.presentation.api.exception_handlers import register_exception_handlers
from app.presentation.api.router import api_router

MIN_SECRET_LENGTH = 32
MAX_SECRET_LENGTH = 256


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncIterator[None]:
    """Подготовка таблиц."""
    secret = os.environ.get("JWT_SECRET_KEY", secrets.token_urlsafe(32))
    if not MIN_SECRET_LENGTH <= len(secret) <= MAX_SECRET_LENGTH:
        message = "JWT_SECRET_KEY must contain 32 to 256 characters"
        raise ValueError(message)
    _app.state.jwt_secret = secret
    Base.metadata.create_all(engine)
    yield
    engine.dispose()


app = FastAPI(lifespan=lifespan)

app.include_router(
    api_router,
    prefix="/api/v1",
)

register_exception_handlers(app)
