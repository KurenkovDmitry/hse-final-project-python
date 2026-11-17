"""Точка входа."""

from fastapi import FastAPI

from _collections_abc import AsyncIterator
from contextlib import asynccontextmanager

from app.container import engine
from app.domain.entities.student import Base
from app.presentation.api.exception_handlers import register_exception_handlers
from app.presentation.api.router import api_router


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncIterator[None]:
    """Подготовка таблиц."""
    Base.metadata.create_all(engine)
    yield
    engine.dispose()


app = FastAPI(lifespan=lifespan)

app.include_router(
    api_router,
    prefix="/api/v1",
)

register_exception_handlers(app)
