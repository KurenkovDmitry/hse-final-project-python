"""Создание обращения."""

from typing import Any

from app.application.ports.storage import RequestStorage


class CreateRequest:
    """Создание обращения."""

    def __init__(self, storage: RequestStorage) -> None:
        """Инициатор."""
        self.storage = storage

    def execute(self, data: dict[str, Any]) -> str:
        """Сохраняем обращение."""
        return self.storage.save(data)
