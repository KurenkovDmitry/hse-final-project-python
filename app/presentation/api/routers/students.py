"""Эндпоинты для работы со студентами."""

from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Path, Query, Response

from app.container import get_student_repository
from app.domain.entities.student import Student
from app.infrastracture.persistence.students import StudentRepository
from app.presentation.api.schemas.student import StudentInput, StudentOutput

router = APIRouter()
Repository = Annotated[StudentRepository, Depends(get_student_repository)]
StudentId = Annotated[int, Path(ge=1, le=2_147_483_647)]


@router.post("", response_model=StudentOutput, status_code=201)
def create_student(student: StudentInput, repository: Repository):
    """Создание."""
    return repository.insert_student(Student(**student.model_dump()))


@router.get("", response_model=list[StudentOutput], status_code=200)
def list_students(
    repository: Repository,
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
    offset: Annotated[int, Query(ge=0, le=1_000_000)] = 0,
) -> list[Student]:
    """Студенты с пагинацией."""
    return repository.list_students(limit=limit, offset=offset)


@router.get("/{student_id}", response_model=StudentOutput, status_code=200)
def get_student(student_id: StudentId, repository: Repository) -> Student:
    """Студент."""
    student = repository.get_student(student_id)
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return student


@router.put("/{student_id}", response_model=StudentOutput, status_code=200)
def update_student(
    student_id: StudentId, student: StudentInput, repository: Repository
) -> Student:
    """Изменеие."""
    updated = repository.update_student(student_id, student.model_dump())
    if updated is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return updated


@router.delete("/{student_id}", status_code=204)
def delete_student(
    student_id: StudentId, repository: Repository
) -> Response:
    """Удаление."""
    if not repository.delete_student(student_id):
        raise HTTPException(status_code=404, detail="Student not found")
    return Response(status_code=204)
