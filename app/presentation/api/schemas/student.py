"""Модели для эндпоинтов."""

from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field, StringConstraints

StudentText = Annotated[
    str, StringConstraints(strip_whitespace=True, min_length=1, max_length=100)
]


class StudentInput(BaseModel):
    """Создание."""

    model_config = ConfigDict(extra="forbid")

    last_name: StudentText
    first_name: StudentText
    faculty: StudentText
    course: StudentText
    grade: int = Field(ge=0, le=100, strict=True)


class StudentOutput(StudentInput):
    """Вывод."""

    model_config = ConfigDict(from_attributes=True)

    id: int
