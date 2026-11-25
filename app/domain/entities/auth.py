"""Пользоватеь и сессии."""

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.domain.entities.student import Base


class User(Base):
    """Пользователь."""

    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True)
    password_hash: Mapped[str] = mapped_column(String(255))


class AuthSession(Base):
    """Сессия."""

    __tablename__ = 'auth_sessions'

    id: Mapped[str] = mapped_column(String(32), primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    expires_at: Mapped[int] = mapped_column(index=True)
