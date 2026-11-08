"""Эндпоинт для обращения абонентов."""

from fastapi import APIRouter

from app.container import create_request
from app.presentation.api.schemas.user import UserRequest

router = APIRouter()


@router.post("", status_code=201)
def add_request(request: UserRequest) -> dict[str, str]:
    """Создаем и созраняем образение."""
    filename = create_request.execute(request.model_dump(mode="json"))
    return {"message": "Обращение сохранено", "filename": filename}
