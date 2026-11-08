"""Сохранение сообщений."""

from pathlib import Path

from app.application.use_cases.create_request import CreateRequest
from app.infrastracture.persistence.json_storage import JsonStorage

create_request = CreateRequest(JsonStorage(Path("request")))
