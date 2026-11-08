"""Обработка ошибок."""

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.infrastracture.exceptions import StorageError


def register_exception_handlers(app: FastAPI) -> None:
    """Обработчик ошибок."""

    @app.exception_handler(StorageError)
    async def storage_error_handler(
        request: Request, exception: StorageError
    ) -> JSONResponse:
        """Обработка ошибки сохранения."""
        return JSONResponse(
            status_code=500,
            content={"detail": str(exception)},
        )
