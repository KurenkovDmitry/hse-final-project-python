"""Хранение пользователя и сессии."""

from collections.abc import Callable

from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from app.domain.entities.auth import AuthSession, User


class AuthRepository:
    """Сессии."""

    def __init__(self, session: Callable[[], Session]) -> None:
        """Инициализация."""
        self.session = session

    def create_user(self, username: str, password_hash: str) -> User:
        """Создание."""
        with self.session() as session:
            user = User(username=username, password_hash=password_hash)
            session.add(user)
            session.commit()
            session.refresh(user)
            return user

    def get_user(self, username: str) -> User | None:
        """Получение."""
        with self.session() as session:
            return session.scalar(
                select(User)
                .where(User.username == username)
            )

    def create_session(self, auth_session: AuthSession, now: int) -> None:
        """Создание сессии."""
        with self.session() as session:
            session.execute(
                delete(AuthSession)
                .where(AuthSession.expires_at <= now)
            )
            session.add(auth_session)
            session.commit()

    def get_session(self, session_id: str) -> AuthSession | None:
        """Получение сессии."""
        with self.session() as session:
            return session.scalar(
                select(AuthSession)
                .join(User, User.id == AuthSession.user_id)
                .where(AuthSession.id == session_id)
            )

    def delete_session(self, session_id: str) -> None:
        """Удаление сессии."""
        with self.session() as session:
            session.execute(
                delete(AuthSession).where(AuthSession.id == session_id)
            )
            session.commit()
