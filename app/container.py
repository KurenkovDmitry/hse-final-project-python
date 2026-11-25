"""Сохранение сообщений."""

from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.application.use_cases.create_request import CreateRequest
from app.infrastracture.persistence.auth import AuthRepository
from app.infrastracture.persistence.json_storage import JsonStorage
from app.infrastracture.persistence.students import StudentRepository

create_request = CreateRequest(JsonStorage(Path("request")))
engine = create_engine(
    "sqlite:///students.db",
    connect_args={"check_same_thread": False},
)
student_repository = StudentRepository(sessionmaker(bind=engine))
auth_repository = AuthRepository(sessionmaker(bind=engine))


def get_student_repository():
    """Передача репозитория."""
    return student_repository


def get_auth_repository() -> AuthRepository:
    """Сессии и пользователи."""
    return auth_repository
