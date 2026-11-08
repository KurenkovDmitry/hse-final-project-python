"""Проверка данных."""

import re
from datetime import date, datetime
from typing import Literal

from pydantic import BaseModel, EmailStr, Field, field_validator


class UserRequest(BaseModel):
    """Модель данных обращения."""

    last_name: str
    first_name: str
    birth_date: date
    phone: str
    email: EmailStr
    reasons: list[
        Literal[
            "нет доступа к сети",
            "не работает телефон",
            "не приходят письма",
        ]
    ] = Field(min_length=1, max_length=3)
    problem_datetime: datetime

    @field_validator("last_name", "first_name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        """Проверка имени."""
        if not re.fullmatch(r"[А-ЯЁ][а-яё]*", value):
            raise ValueError(
                "Имя и фамилия должны быть с заглавной буквы "
                "и содержать только кириллицу"
            )
        return value

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, value: str) -> str:
        """Проверка телефона."""
        if not re.fullmatch(r"(?:\+7|8)[0-9]{10}", value):
            raise ValueError(
                "Телефон должен быть в формате +7XXXXXXXXXX или 8XXXXXXXXXX"
            )
        return value

    @field_validator("birth_date")
    @classmethod
    def validate_birth_date(cls, value: date) -> date:
        """Проверка даты рождения."""
        if value > date.today():
            raise ValueError("Дата рождения не может быть больше текущей")
        return value

    @field_validator("problem_datetime")
    @classmethod
    def validate_problem_datetime(cls, value: datetime) -> datetime:
        """Проверка даты огнаружения пробелемы."""
        if value > datetime.now(value.tzinfo):
            raise ValueError(
                "Дата обнаружения проблемы не может быть больше текущей"
            )
        return value
