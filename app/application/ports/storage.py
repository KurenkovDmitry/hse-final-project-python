"""Интерфейс для сохранения."""

from typing import Any, Protocol


class RequestStorage(Protocol):
    """Сохранение обращений."""

    def save(self, data: dict[str, Any]) -> str:
        """Сохранение + возврат имени файла."""
        ...
