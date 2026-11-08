"""Сохранение обращений."""

import json
from pathlib import Path
from typing import Any
from uuid import uuid4

from app.infrastracture.exceptions import StorageError


class JsonStorage:
    """Сохранение обращений."""

    def __init__(self, folder: Path) -> None:
        """Инициатор."""
        self.folder = folder

    def save(self, data: dict[str, Any]) -> str:
        """Созраняем в JSON формате."""
        filename = f"{uuid4().hex}.json"

        try:
            self.folder.mkdir(parents=True, exist_ok=True)
            with (self.folder / filename).open("w", encoding="utf-8") as file:
                json.dump(data, file, ensure_ascii=False, indent=4)
        except OSError as error:
            raise StorageError("Не удалось сохранить") from error

        return filename
