"""Операции для студентов."""

import csv
from collections.abc import Callable, Iterable
from pathlib import Path

from sqlalchemy import Engine, func, select
from sqlalchemy.orm import Session

from app.domain.entities.student import Base, Student

CSV_FIELDS = (
    "Фамилия",
    "Имя",
    "Факультет",
    "Курс",
    "Оценка",
)


class StudentRepository:
    """insert + select."""

    def __init__(self, session: Callable[[], Session]) -> None:
        """Инициализация."""
        self.session = session

    def create_tables(self, engine: Engine) -> None:
        """Создание таблиц."""
        Base.metadata.create_all(engine)

    def insert_student(self, student: Student) -> Student:
        """Добавление студента."""
        with self.session() as session:
            session.add(student)
            session.commit()
            session.refresh(student)
            return student

    def insert_students(self, students: Iterable[Student]) -> int:
        """Добавление ряда студентов."""
        students_to_ins = list(students)
        with self.session() as session:
            for student in students_to_ins:
                session.add(student)
            session.commit()
        return len(students_to_ins)

    def load_csv(self, csv_path: Path) -> int:
        """Загрузка из файла."""
        with csv_path.open(encoding="utf-8", newline="") as file:
            reader = csv.DictReader(file)
            if tuple(reader.fieldnames or ()) != CSV_FIELDS:
                raise ValueError("В CSV не студенты")

            students = [
                Student(
                    last_name=row["Фамилия"].strip(),
                    first_name=row["Имя"].strip(),
                    faculty=row["Факультет"].strip(),
                    course=row["Курс"].strip(),
                    grade=int(row["Оценка"]),
                )
                for row in reader
            ]

        return self.insert_students(students)

    def select_by_faculty(self, faculty: str) -> list[Student]:
        """Студенты по факультативу."""
        with self.session() as session:
            return list(
                session.scalars(
                    select(Student)
                    .where(Student.faculty == faculty)
                    .order_by(Student.id)
                )
            )

    def select_unique_courses(self) -> list[str]:
        """Уникальные курсы."""
        with self.session() as session:
            return list(
                session.scalars(
                    select(Student.course).distinct().order_by(Student.course)
                )
            )

    def select_by_course_below_grade(
        self, course: str, maximum_grade: int = 30
    ) -> list[Student]:
        """Студенты с оценкой ниже заданной."""
        with self.session() as session:
            return list(
                session.scalars(
                    select(Student)
                    .where(
                        Student.course == course,
                        Student.grade < maximum_grade,
                    )
                    .order_by(Student.id)
                )
            )

    def select_average_by_faculty(self, faculty: str) -> float | None:
        """Срений бал в условияъ факультета."""
        with self.session() as session:
            average = session.scalar(
                select(func.avg(Student.grade)).where(
                    Student.faculty == faculty
                )
            )
            return float(average) if average is not None else None
